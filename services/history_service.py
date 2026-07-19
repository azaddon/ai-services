import logging
from datetime import datetime, timezone

from services.config import Config

logger = logging.getLogger(__name__)


class HistoryUnavailableError(RuntimeError):
    pass


class HistoryService:
    _client = None
    _collection = None

    @classmethod
    def enabled(cls) -> bool:
        return bool(Config.MONGO_URI)

    @classmethod
    def _get_collection(cls):
        if not cls.enabled():
            raise HistoryUnavailableError("MongoDB history is not configured")
        if cls._collection is None:
            from pymongo import ASCENDING, DESCENDING, MongoClient

            cls._client = MongoClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=Config.MONGO_CONNECT_TIMEOUT_MS,
                connectTimeoutMS=Config.MONGO_CONNECT_TIMEOUT_MS,
                retryWrites=True,
            )
            cls._client.admin.command("ping")
            cls._collection = cls._client[Config.MONGO_DATABASE]["failure_analyses"]
            cls._collection.create_index([("createdAt", DESCENDING)])
            cls._collection.create_index([("context.testName", ASCENDING)])
            cls._collection.create_index([("context.environment", ASCENDING)])
        return cls._collection

    @classmethod
    def save(cls, request, analysis) -> str | None:
        if not cls.enabled():
            return None
        context = request.context.model_dump(
            exclude={"screenshotBase64", "screenshotPath", "videoPath", "pageHtml"},
            exclude_none=True,
        )
        document = {
            "createdAt": datetime.now(timezone.utc),
            "context": context,
            "analysis": analysis.model_dump(),
        }
        try:
            return str(cls._get_collection().insert_one(document).inserted_id)
        except Exception:
            logger.exception("Could not persist failure analysis history")
            return None

    @classmethod
    def list(cls, skip: int, limit: int):
        collection = cls._get_collection()
        cursor = collection.find({}, {"context.logs": 0}).sort("createdAt", -1)
        items = [cls._serialize(item) for item in cursor.skip(skip).limit(limit)]
        return {"items": items, "skip": skip, "limit": limit}

    @classmethod
    def analytics(cls):
        collection = cls._get_collection()
        pipeline = [
            {"$group": {
                "_id": None,
                "total": {"$sum": 1},
                "averageConfidence": {"$avg": "$analysis.confidence"},
            }},
            {"$project": {"_id": 0}},
        ]
        summary = next(collection.aggregate(pipeline), None)
        return summary or {"total": 0, "averageConfidence": None}

    @staticmethod
    def _serialize(document):
        document["id"] = str(document.pop("_id"))
        if isinstance(document.get("createdAt"), datetime):
            document["createdAt"] = document["createdAt"].isoformat()
        return document

    @classmethod
    def close(cls):
        if cls._client is not None:
            cls._client.close()
        cls._client = None
        cls._collection = None

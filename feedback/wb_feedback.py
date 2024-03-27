import requests

from datetime import datetime, timedelta
from pydantic import BaseModel

API_URL = "https://feedbacks2.wb.ru/feedbacks/v1/"


class FeedbackListDTO(BaseModel):
    valuation: str
    valuationSum: int
    feedbackCount: int
    feedbacks: list["FeedbacksDTO"] | None


class FeedbacksDTO(BaseModel):
    id: str
    wbUserId: int
    text: str | None
    productValuation: int
    createdDate: datetime


class Feedback:
    def __init__(
        self,
        sku: str | int,
        feedbacks: FeedbackListDTO | None = None
    ) -> None:
        self.product_sku = str(sku)
        self.feedbacks = feedbacks if feedbacks else self.__get_feedbacks()

    def negative_feedbacks(self, min_rate: int = 3):
        if not self.feedbacks.feedbacks:
            return Feedback(self.product_sku, self.feedbacks)

        filtered_feedbacks = [
            x for x in self.feedbacks.feedbacks if x.productValuation <= min_rate
        ]
        new_feedback = self.feedbacks
        new_feedback.feedbacks = filtered_feedbacks
        return Feedback(self.product_sku, new_feedback)

    def by_time(self, seconds: int = 0, minutes: int = 0, hours: int = 12):
        if not self.feedbacks.feedbacks:
            return Feedback(self.product_sku, self.feedbacks)

        past = datetime.today() - timedelta(seconds=seconds, hours=hours, minutes=minutes)

        filtered_feedbacks = [
            x for x in self.feedbacks.feedbacks
            if x.createdDate.timestamp() >= past.timestamp()
        ]
        new_feedback = self.feedbacks
        new_feedback.feedbacks = filtered_feedbacks
        return Feedback(self.product_sku, new_feedback)

    def all(self):
        return self.feedbacks

    def get_sku(self):
        return self.product_sku

    def __get_feedbacks(self) -> FeedbackListDTO:
        feedbacks = requests.get(url=self.__get_api_url())
        return FeedbackListDTO(**feedbacks.json())

    def __get_api_url(self) -> str:
        return API_URL + self.product_sku

from typing import List

import strawberry


@strawberry.type
class Review:
    id: int
    body: str


def get_reviews(root: "Book") -> List[Review]:
    return [
        Review(id=id_, body=f"A review for {root.id}")
        for id_ in range(root.reviews_count)
    ]


@strawberry.federation.type(keys=["id"])
class Book:
    id: strawberry.ID
    reviews_count: int
    reviews: List[Review] = strawberry.field(resolver=get_reviews)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        # here we could fetch the book from the database
        # or even from an API
        return Book(id=id, reviews_count=3)


@strawberry.type
class Query:
    _hi: str = strawberry.field(resolver=lambda: "Hello World!")


schema = strawberry.federation.Schema(
    query=Query, types=[Book, Review], enable_federation_2=True
)

from fastapi import HTTPException, status


class AuthorNotFound(HTTPException):
    def __init__(self, route: str) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Author Not Found Error In Route {route}"


class BooksNotFound(HTTPException):
    def __init__(self, route: str) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Book Not Found Error In Route {route}"


class DeleteSuccessful(HTTPException):
    def __init__(self, route: str) -> None:
        self.status_code = status.HTTP_200_OK
        self.detail = f"Delete Book Successfully {route}"

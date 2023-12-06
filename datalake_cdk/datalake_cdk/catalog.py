from aws_cdk import aws_glue as glue
from constructs import Construct


class Crawler(Construct):
    def __init__(
        self,
        scope: "Construct",
        id: "str",
        role_arn: str,
        database_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        glue.CfnCrawler(
            self,
            id,
            role=role_arn,
            database_name=database_name,
        )

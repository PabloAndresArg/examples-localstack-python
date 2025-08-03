
from fastapi import HTTPException

class DynamoService:
    """Service class for handling DynamoDB operations."""
    
    def __init__(self, table):
        """Initialize DynamoDB service.
        Args:
            table: boto3.Table: DynamoDB table resource
        """
        self.table = table

    def get_all_records(self) -> list:
        """ Get all records from DynamoDB table.
        Returns: (list): List of records from DynamoDB
        Raises: HTTPException: If query fails
        """
        try:
            records = []
            response = self.table.scan()
            records.extend(response.get('Items', []))

            while 'LastEvaluatedKey' in response:
                """
                Bring more records:
                In DynamoDB, the scan method returns a LastEvaluatedKey when the query results exceed the DynamoDB response size limit. 
                This occurs in the following cases:

                When the total data size exceeds 1 MB
                When the number of items exceeds the 'Limit' specified in the query
                When DynamoDB needs to paginate the results due to internal service limitations
                """
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                records.extend(response.get('Items', []))

            return records
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def format_records_as_text(self, records: list) -> str:
        """ Format records as text.
        Args: records (list): List of records to format
        Returns: (str): Formatted text
        """
        return ''.join(
            f"ID: {r.get('id', 'N/A')}, Body: {r.get('body', 'N/A')}\n"
            for r in records
        )

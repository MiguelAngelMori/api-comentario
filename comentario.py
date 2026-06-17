import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]      # <-- CAMBIO 2 (lee la variable de entorno)

    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }

    # Guardar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # ---------- CAMBIO 3: Ingesta Push -> grabar el json como archivo en S3 ----------
    s3 = boto3.client('s3')
    s3_key = f"comentarios/{tenant_id}/{uuidv1}.json"
    s3.put_object(
        Bucket=nombre_bucket,
        Key=s3_key,
        Body=json.dumps(comentario, ensure_ascii=False),
        ContentType='application/json'
    )

    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'archivo_s3': f"s3://{nombre_bucket}/{s3_key}",
        'response': response
    }

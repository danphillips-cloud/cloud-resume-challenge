import functions_framework
from google.cloud import firestore
import json

# Initialize Firestore client
db = firestore.Client()

@functions_framework.http
def visitor_counter(request):
    """
    HTTP Cloud Function for visitor counter.
    Increments and returns visitor count from Firestore.
    """
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Reference to visitor counter document
        doc_ref = db.collection('counters').document('visitors')
        
        # Use transaction for atomic increment
        @firestore.transactional
        def update_counter(transaction):
            snapshot = doc_ref.get(transaction=transaction)
            
            if snapshot.exists:
                current_count = snapshot.get('count')
                new_count = current_count + 1
            else:
                # Initialize if doesn't exist
                new_count = 1
            
            transaction.set(doc_ref, {
                'count': new_count,
                'lastUpdated': firestore.SERVER_TIMESTAMP
            })
            
            return new_count
        
        # Execute transaction
        transaction = db.transaction()
        count = update_counter(transaction)
        
        return (json.dumps({'count': count}), 200, headers)
        
    except Exception as e:
        print(f'Error: {str(e)}')
        return (json.dumps({'error': 'Internal server error'}), 500, headers)
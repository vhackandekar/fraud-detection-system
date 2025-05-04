from flask import Flask, render_template, request, jsonify
from src.data_processor import TransactionProcessor

app = Flask(__name__)
processor = TransactionProcessor()

@app.route('/')
def home():
    # Initialize default stats if none exist
    stats = {
        'total_transactions': 0,
        'fraud_cases': 0,
        'normal_cases': 0,
        'average_amount': 0.00,
        'fraud_rate': 0.00
    }
    
    # Get actual stats from processor
    try:
        processor_stats = processor.get_statistics()
        stats.update(processor_stats)
    except Exception as e:
        print(f"Error getting statistics: {e}")
    
    return render_template('index.html', stats=stats)

@app.route('/analyze', methods=['POST'])
def analyze_transaction():
    data = request.get_json()
    result = processor.process_transaction(data)
    return jsonify(result)

@app.route('/stats')
def get_stats():
    try:
        stats = processor.get_statistics()  # Get latest stats from processor
        if not stats:
            stats = {
                'total_transactions': 0,
                'fraud_cases': 0,
                'normal_cases': 0,
                'average_amount': 0.00,
                'fraud_rate': 0.00
            }
        
        # Calculate fraud rate and average amount if not provided
        if stats['total_transactions'] > 0:
            stats['fraud_rate'] = (stats['fraud_cases'] / stats['total_transactions']) * 100
            if 'average_amount' not in stats:
                stats['average_amount'] = stats.get('total_amount', 0) / stats['total_transactions']
        
        return jsonify(stats)
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Real-Time Fraud Detection System

A sophisticated web-based application that provides real-time transaction monitoring and fraud detection using statistical analysis and machine learning algorithms. The system processes financial transactions, calculates risk scores, and provides immediate feedback on potential fraudulent activities.

## Features

### Real-time Transaction Analysis
- Instant transaction risk assessment
- Anomaly detection using statistical analysis
- Real-time risk score calculation
- Visual risk gauge representation
- Transaction amount threshold monitoring

### Interactive Dashboard
- Live statistics with auto-refresh
- Transaction count monitoring
- Fraud case tracking
- Average transaction amount
- Real-time fraud rate calculation
- Animated stat cards with hover effects

### Machine Learning Integration
- Feature normalization using Z-scores
- Statistical threshold calculations
- Historical data analysis
- Pattern recognition for fraud detection

## Technical Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- NumPy (Numerical Computing)
- Pandas (Data Processing)
- Scikit-learn (Machine Learning)

### Frontend
- HTML5/CSS3
- JavaScript (ES6+)
- Plotly.js (Visualization)
- jQuery
- Font Awesome (Icons)

## Project Structure
```
fraud-detection-system/
├── src/
│   ├── anomaly_detector.py    # Machine learning model implementation
│   └── data_processor.py      # Transaction processing logic
├── static/
│   ├── main.js               # Frontend JavaScript
│   └── style.css             # Styling
├── templates/
│   └── index.html            # Main dashboard template
├── data/
│   └── creditcard.csv        # Training dataset
├── app.py                    # Flask application
└── requirements.txt          # Python dependencies
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fraud-detection-system.git
cd fraud-detection-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure you have the credit card dataset in the data folder:
```
data/creditcard.csv
```

5. Run the application:
```bash
python app.py
```

Access the application at `http://localhost:5000`

## API Endpoints

### GET /
- Returns the main dashboard
- Displays real-time statistics and transaction input form

### POST /analyze
- Analyzes a transaction for fraud
- Request body: JSON with transaction details
- Returns: Risk assessment and fraud probability

### GET /stats
- Provides current system statistics
- Returns: JSON with transaction counts, fraud rates, and averages

## System Features

### Transaction Processing
- Real-time transaction validation
- Risk score calculation (0-1 scale)
- Fraud probability assessment
- Statistical anomaly detection

### Statistics Tracking
- Total transaction count
- Fraud case count
- Normal transaction count
- Average transaction amount
- Current fraud rate
- Recent transaction metrics

### Visualization
- Risk score gauge
- Transaction status alerts
- Interactive statistics cards
- Real-time updates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Credit card fraud detection dataset
- Scikit-learn community
- Flask framework documentation
- Plotly.js visualization library

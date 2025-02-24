# README for Synthetic Data Generator

## Overview

The Synthetic Data Generator project is designed to create synthetic datasets containing Personal Identifiable Information (PII). This project utilizes Python libraries to generate realistic fake data, which can be used for testing, training, or research purposes without compromising real personal information.

## Project Structure

```
synthetic-data-generator
├── src
│   ├── generate_data.py       # Main script for generating synthetic data
│   └── utils
│       └── __init__.py        # Utility functions for data generation
├── data
│   └── README.md              # Documentation for the generated data
├── requirements.txt           # Project dependencies
└── README.md                  # Project overview and instructions
```

## Usage Instructions

1. **Install Dependencies**: Before running the project, ensure that you have all the required libraries installed. You can do this by running:
   ```
   pip install -r requirements.txt
   ```

2. **Generate Data**: To generate synthetic data, run the `generate_data.py` script located in the `src` directory. This will create a CSV file containing the generated PII in the `data` folder.

3. **Check Generated Data**: After running the script, you can find the generated CSV file in the `data` folder. Refer to the `data/README.md` for more details on the structure and contents of the generated files.

## Contributing

Contributions to enhance the functionality or improve the project are welcome. Please feel free to submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
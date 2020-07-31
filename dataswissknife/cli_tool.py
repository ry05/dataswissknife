""" The Command Line Tool that actually runs """

__all__ = [
	'main_code',
	'clean_data',
	'load_data',
	'preprocess_data',
	'classification_modelling',
	'visualize_data',
	'log_tracker',
]

from dataswissknife import main_code

def main():
	main_code.initiate_tool()
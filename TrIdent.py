import argparse
import subprocess
import sys

def run_script(script_name, args):
    # Convert all arguments to strings
    command = ['python', script_name] + [str(arg) for arg in args]
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser(description='Wrapper for different modes')
    parser.add_argument('-mode', required=True, help='Mode of operation')
    parser.add_argument('-pref', type=str, help='File prefix for image_generation_ms and image_generation_vcf')
    parser.add_argument('-outFile', type=str, help='Output file name for image_generation_ms')
    parser.add_argument('-nHap', type=int, help='Number of haplotypes for image_generation_ms and image_generation_vcf')
    parser.add_argument('-subFolder', type=str, help='Subfolder name for image_generation_ms')
    parser.add_argument('-n', type=int, help='Number of files for image_generation_ms and image_generation_vcf')
    parser.add_argument('-start', type=int, help='Start number of files for image_generation_ms and image_generation_vcf')
    parser.add_argument('-stop', type=int, help='Stop number of files for image_generation_vcf')
    parser.add_argument('-imgDim', type=int, help='Image dimension for image_generation_ms and image_generation_vcf')
    parser.add_argument('-fileName', type=str, help='File name for preprocess_vcf and prediction')
    parser.add_argument('-outFolder', type=str, help='Output folder for preprocess_vcf')
    parser.add_argument('-split', type=float, help='Train/test split for train mode')
    parser.add_argument('-modelName', type=str, help='Name of model for train and prediction')
    parser.add_argument('-Sw', type=str, help='Sweep file for train mode')
    parser.add_argument('-Ne', type=str, help='Neutral file for train mode')
    parser.add_argument('-subfolder', type=str, help='Subfolder for image_generation_vcf')
    parser.add_argument('-outDat', type=str, help='Output dataset name for image_generation_vcf')

    args = parser.parse_args()
    mode = args.mode

    # Validate arguments for each mode
    if mode == 'image_generation_ms':
        required_args = ['pref', 'outFile', 'nHap', 'subFolder', 'n', 'start', 'imgDim']
        invalid_args = ['fileName', 'outFolder', 'split', 'modelName', 'Sw', 'Ne', 'stop', 'outDat']
    elif mode == 'train':
        required_args = ['Sw', 'Ne', 'split', 'modelName']
        invalid_args = ['pref', 'outFile', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'stop', 'outDat']
    elif mode == 'preprocess_vcf':
        required_args = ['fileName', 'outFolder']
        invalid_args = ['pref', 'outFile', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'split', 'modelName', 'Sw', 'Ne', 'stop', 'outDat']
    elif mode == 'image_generation_vcf':
        required_args = ['subfolder', 'nHap', 'pref', 'start', 'stop', 'imgDim', 'outDat']
        invalid_args = ['fileName', 'outFolder', 'split', 'modelName', 'Sw', 'Ne']
    elif mode == 'prediction':
        required_args = ['fileName', 'modelName']
        invalid_args = ['pref', 'outFile', 'nHap', 'subFolder', 'n', 'start', 'imgDim', 'split', 'Sw', 'Ne', 'stop', 'outDat']
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

    # Check for missing required arguments
    missing_args = [arg for arg in required_args if getattr(args, arg) is None]
    if missing_args:
        print(f"Error: Missing required arguments for '{mode}' mode: {', '.join(missing_args)}")
        sys.exit(1)

    # Check for invalid arguments
    invalid_args_provided = [arg for arg in invalid_args if getattr(args, arg) is not None]
    if invalid_args_provided:
        print(f"Error: {' '.join(invalid_args_provided)} is/are invalid for '{mode}' mode")
        sys.exit(1)

    # Map modes to their respective scripts
    script_mapping = {
        'image_generation_ms': 'image_generation_ms.py',
        'train': 'train.py',
        'preprocess_vcf': 'preprocess_vcf.py',
        'image_generation_vcf': 'image_generation_vcf.py',
        'prediction': 'prediction.py'
    }

    if mode in script_mapping:
        script_name = script_mapping[mode]
        # Collect required arguments based on mode
        script_args = [getattr(args, arg) for arg in required_args]
        run_script(script_name, script_args)
    else:
        print(f"Error: Mode '{mode}' is invalid")
        sys.exit(1)

if __name__ == '__main__':
    main()


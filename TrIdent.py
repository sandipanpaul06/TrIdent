import sys
import subprocess

def run_script(script_name, args):
    try:
        subprocess.run([sys.executable, script_name] + args)
    except Exception as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a valid script name.")
        sys.exit(1)

    # Map command-line arguments to specific scripts
    scripts = {
        "image_generation_ms": "image_generation_ms.py",    
        "train": "train.py",                  
        "preprocess_VCF": "preprocess_VCF.py",         
        "image_generation_vcf": "image_generation_vcf.py",   
        "prediction": "prediction.py"              
    }

    # Get the script argument and pass the rest as additional arguments
    script_to_run = sys.argv[1]
    additional_args = sys.argv[2:]

    if script_to_run in scripts:
        run_script(scripts[script_to_run], additional_args)
    else:
        print(f"Unknown script: {script_to_run}. Please use one of the following: {', '.join(scripts.keys())}")


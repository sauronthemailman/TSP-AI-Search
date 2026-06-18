"""
RunParallel.py - Run all algorithms in parallel for 1 hour

Spawns 4 processes (one per algorithm) that continuously run on all city files.
After 1 hour, finds the best tour for each city and renames to submission format.

Usage: python RunParallel.py
"""

import os
import subprocess
import sys
import re
import glob
import time
import multiprocessing
from multiprocessing import Process, Manager

# Configuration
USER_NAME = "your_username"
RUN_TIME_SECONDS = 1800  

CITY_FILES = [
    "AISearchfile012.txt",
    "AISearchfile017.txt",
    "AISearchfile021.txt",
    "AISearchfile026.txt",
    "AISearchfile042.txt",
    "AISearchfile048.txt",
    "AISearchfile058.txt",
    "AISearchfile175.txt",
    "AISearchfile180.txt",
    "AISearchfile535.txt"
]

ALGORITHMS = ["AlgAbasic", "AlgAenhanced", "AlgBbasic", "AlgBenhanced"]

def parse_tour_length(filepath):
    """Extract tour length from a tour file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        match = re.search(r'TOUR LENGTH = (\d+)', content)
        if match:
            return int(match.group(1))
    except:
        pass
    return float('inf')

def run_algorithm_loop(alg_name, user_folder, end_time, run_counts, best_lengths):
    """Continuously run one algorithm on all city files until time runs out"""
    script = f"{alg_name}.py"
    
    while time.time() < end_time:
        for city in CITY_FILES:
            if time.time() >= end_time:
                break
            
            try:
                # Calculate remaining time
                remaining = end_time - time.time()
                if remaining <= 0:
                    break
                
                # Run the algorithm
                result = subprocess.run(
                    [sys.executable, script, city],
                    capture_output=True,
                    text=True,
                    timeout=min(120, remaining),  # Max 2 min per run or remaining time
                    cwd=user_folder
                )
                
                # Update run count
                key = f"{alg_name}_{city}"
                run_counts[key] = run_counts.get(key, 0) + 1
                
                # Check if we got a new best
                city_base = city.replace('.txt', '')
                group = "AlgA" if alg_name.startswith("AlgA") else "AlgB"
                
                # Find the most recent tour file
                pattern = os.path.join(user_folder, f"{alg_name}_{city_base}_*.txt")
                matches = glob.glob(pattern)
                if matches:
                    matches.sort(key=os.path.getmtime, reverse=True)
                    length = parse_tour_length(matches[0])
                    
                    # Track best for this group+city
                    best_key = f"{group}_{city}"
                    current_best = best_lengths.get(best_key, float('inf'))
                    if length < current_best:
                        best_lengths[best_key] = length
                        print(f"[{alg_name}] {city}: {length} <- NEW BEST!")
                    
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                pass

def main():
    print("=" * 60)
    print("TSP Parallel Runner")
    print(f"Running all algorithms in parallel for {RUN_TIME_SECONDS // 60} minutes")
    print("=" * 60)
    
    if not os.path.isdir(USER_NAME):
        print(f"ERROR: Folder '{USER_NAME}' not found!")
        sys.exit(1)
    
    user_folder = os.path.abspath(USER_NAME)
    
    # Clean up existing tour files
    print("\nCleaning up existing tour files...")
    count = 0
    for f in os.listdir(user_folder):
        if f.endswith('.txt') and 'AISearchfile' in f:
            os.remove(os.path.join(user_folder, f))
            count += 1
    print(f"Deleted {count} files")
    
    # Shared state between processes
    manager = Manager()
    run_counts = manager.dict()
    best_lengths = manager.dict()
    
    # Start time and end time
    start_time = time.time()
    end_time = start_time + RUN_TIME_SECONDS
    
    print(f"\nStarting parallel execution at {time.strftime('%H:%M:%S')}")
    print(f"Will run until {time.strftime('%H:%M:%S', time.localtime(end_time))}")
    print("=" * 60)
    
    # Start a process for each algorithm
    processes = []
    for alg in ALGORITHMS:
        p = Process(target=run_algorithm_loop, args=(alg, user_folder, end_time, run_counts, best_lengths))
        p.start()
        processes.append((alg, p))
        print(f"Started process for {alg}")
    
    # Wait for all processes to finish
    print("\nRunning... (press Ctrl+C to stop early)\n")
    
    try:
        for alg, p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n\nStopping early...")
        for alg, p in processes:
            p.terminate()
            p.join()
    
    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"Finished after {elapsed / 60:.1f} minutes")
    print("=" * 60)
    
    # Print run statistics
    print("\nRun counts per algorithm/city:")
    for alg in ALGORITHMS:
        total = sum(run_counts.get(f"{alg}_{city}", 0) for city in CITY_FILES)
        print(f"  {alg}: {total} total runs")
    
    # Find and rename best tours
    print("\n" + "=" * 60)
    print("Finding best tours and renaming to submission format...")
    print("=" * 60)
    
    for group in ['AlgA', 'AlgB']:
        print(f"\n{group}:")
        
        for city in CITY_FILES:
            city_base = city.replace('.txt', '')
            
            # Find all tour files for this group and city
            pattern = os.path.join(user_folder, f"{group}*_{city_base}_*.txt")
            matches = glob.glob(pattern)
            
            if not matches:
                print(f"  {city_base}: NO TOURS FOUND!")
                continue
            
            # Find the best one
            best_file = None
            best_length = float('inf')
            
            for f in matches:
                length = parse_tour_length(f)
                if length < best_length:
                    best_length = length
                    best_file = f
            
            # Rename best to submission format
            final_name = f"{group}_{city_base}.txt"
            final_path = os.path.join(user_folder, final_name)
            
            if best_file:
                # Delete all non-best files
                for f in matches:
                    if f != best_file:
                        os.remove(f)
                
                # Rename best file
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(best_file, final_path)
                print(f"  {final_name}: {best_length} (from {len(matches)} tours)")
            else:
                print(f"  {final_name}: FAILED")
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    for group in ['AlgA', 'AlgB']:
        print(f"\n{group}:")
        total = 0
        for city in CITY_FILES:
            city_base = city.replace('.txt', '')
            fname = f"{group}_{city_base}.txt"
            fpath = os.path.join(user_folder, fname)
            if os.path.exists(fpath):
                length = parse_tour_length(fpath)
                total += length
                print(f"  {fname}: {length}")
            else:
                print(f"  {fname}: MISSING!")
        print(f"  TOTAL: {total}")
    
    print("\n" + "=" * 60)
    print("DONE! Now run: python validate_before_handin.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
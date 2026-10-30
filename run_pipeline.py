import subprocess
import sys


def run_step(description, command):
    print(f"\n{'=' * 60}", flush=True)
    print(description, flush=True)
    print(f"{'=' * 60}", flush=True)

    result = subprocess.run(command, check=False)

    if result.returncode != 0:
        print(f"\nLOI: Buoc '{description}' that bai.")
        sys.exit(result.returncode)


def main():
    run_step(
        "BUOC 1: XU LY VA KIEM TRA CHAT LUONG DU LIEU",
        [sys.executable, "-m", "src.pipeline"],
    )

    run_step(
        "BUOC 2: NAP DU LIEU VAO KHO",
        [sys.executable, "-m", "src.etl.load_warehouse"],
    )

    print("\nHOAN TAT PIPELINE.")


if __name__ == "__main__":
    main()

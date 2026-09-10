import sys

if __name__ == "__main__":
    try:
        from .cli import main
        main()
    except KeyboardInterrupt:
        sys.exit("Process interrupted by user\n")
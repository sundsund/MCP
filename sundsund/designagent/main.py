from diagrams import Diagram
from diagrams.gcp.compute import GCE

def main():
    with Diagram("My GCP Architecture", show=False, filename="my_architecture"):
        GCE("My GCP Node")

if __name__ == "__main__":
    main()

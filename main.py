from orchestrator import Orchestrator


def main():

    dataset_source = input("Enter dataset path or Kaggle dataset name: ")

    orchestrator = Orchestrator()

    orchestrator.run(dataset_source)


if __name__ == "__main__":
    main()
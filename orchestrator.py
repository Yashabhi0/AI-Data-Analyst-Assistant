from agents.data_loader_agent import DataLoaderAgent
from agents.profiling_agent import ProfilingAgent
from agents.visualization_agent import VisualizationAgent
from agents.pattern_detection_agent import PatternDetectionAgent
from agents.outlier_detection_agent import OutlierDetectionAgent
from agents.insight_agent import InsightAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_agent import ReportAgent


class Orchestrator:

    def __init__(self):

        self.loader = DataLoaderAgent()
        self.profiler = ProfilingAgent()
        self.visualizer = VisualizationAgent()
        self.pattern_detector = PatternDetectionAgent()
        self.outlier_detector = OutlierDetectionAgent()
        self.insight_engine = InsightAgent()
        self.recommender = RecommendationAgent()
        self.reporter = ReportAgent()

    def run(self, dataset_source):

        print("Starting AI Data Analysis Pipeline...\n")

        # Step 1 — Load dataset
        df = self.loader.load(dataset_source)

        if df is None:
            print("Dataset loading failed.")
            return

        print("Dataset loaded successfully.\n")

        # Step 2 — Profiling
        profile = self.profiler.analyze(df)

        # Step 3 — Visualizations
        self.visualizer.generate(df)

        # Step 4 — Pattern detection
        patterns = self.pattern_detector.detect(df)

        # Step 5 — Outlier detection
        outliers = self.outlier_detector.detect(df)

        # Step 6 — Insight generation
        insights = self.insight_engine.generate(profile, patterns, outliers)

        # Step 7 — Recommendations
        recommendations = self.recommender.generate(profile, patterns, outliers)

        # Step 8 — Report generation
        self.reporter.generate(profile, insights, recommendations)

        print("\nAnalysis Complete.")
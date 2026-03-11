from agents.data_loader_agent import DataLoaderAgent
from agents.data_cleaning_agent import DataCleaningAgent
from agents.profiling_agent import ProfilingAgent
from agents.visualization_agent import VisualizationAgent
from agents.pattern_detection_agent import PatternDetectionAgent
from agents.outlier_detection_agent import OutlierDetectionAgent
from agents.insight_agent import InsightAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_agent import ReportAgent
from agents.llm_explainer_agent import LLMExplainerAgent


class Orchestrator:

    def __init__(self):

        self.loader = DataLoaderAgent()
        self.cleaner = DataCleaningAgent()
        self.profiler = ProfilingAgent()
        self.visualizer = VisualizationAgent()
        self.pattern_detector = PatternDetectionAgent()
        self.outlier_detector = OutlierDetectionAgent()
        self.insight_engine = InsightAgent()
        self.recommender = RecommendationAgent()
        self.reporter = ReportAgent()
        self.llm_explainer = LLMExplainerAgent()

    def run(self, dataset_source):

        print("Starting AI Data Analysis Pipeline...\n")

        # -------------------------------
        # Step 1 — Load dataset
        # -------------------------------
        df = self.loader.load(dataset_source)

        if df is None:
            print("Dataset loading failed.")
            return None

        print("Dataset loaded successfully.\n")

        # -------------------------------
        # Step 2 — Handle missing values
        # -------------------------------
        df, missing_summary = self.cleaner.handle_missing_values(df)

        # -------------------------------
        # Step 3 — Profiling
        # -------------------------------
        profile = self.profiler.analyze(df)

        # -------------------------------
        # Step 4 — Visualizations
        # -------------------------------
        self.visualizer.generate(df)

        # -------------------------------
        # Step 5 — Pattern detection
        # -------------------------------
        patterns = self.pattern_detector.detect(df)

        # -------------------------------
        # Step 6 — Outlier detection
        # -------------------------------
        outliers = self.outlier_detector.detect(df)

        # -------------------------------
        # Step 7 — Insight generation
        # -------------------------------
        insights = self.insight_engine.generate(profile, patterns, outliers)

        # -------------------------------
        # Step 8 — Recommendations
        # -------------------------------
        recommendations = self.recommender.generate(profile, patterns, outliers)

        # -------------------------------
        # Step 9 — AI Explanation
        # -------------------------------
        ai_explanation = self.llm_explainer.explain(
            profile,
            insights,
            recommendations
        )

        # -------------------------------
        # Step 10 — Report
        # -------------------------------
        self.reporter.generate(
            profile,
            insights,
            recommendations
        )

        print("\nAnalysis Complete.")

        return df, profile, insights, recommendations, ai_explanation, missing_summary
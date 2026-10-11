from .signal_fusion import SignalFusion
from .confidence import ConfidenceCalculator
from .conflict_resolver import ConflictResolver
from .summary import SummaryBuilder
from .normalizer import ScoreNormalizer 
from .models import ConfluenceResult

class ConfluenceEngine:
     def evaluate(
               self,
               signals
     ):
          fusion = SignalFusion()
          bullish, bearish, reasons = fusion.combine(
               signals
          )
          maximum = bullish + bearish

          bullish_score = ScoreNormalizer.normalize(
               bullish, 
               maximum
          )

          bearish_score = ScoreNormalizer.normalize(
               bearish,
               maximum
          )

          confidence = ConfidenceCalculator().calculate(
               bullish,

               bearish
          )

          direction = ConflictResolver().resolve(
               bullish,

               bearish
          )
          SummaryBuilder().build(
               direction,

               confidence,

               reasons
          )

          return ConfluenceResult(
               direction,
               max(
                bullish_score,

                bearish_score
               ),
               confidence,

               bullish_score,

               bearish_score,

               reasons

          )
     
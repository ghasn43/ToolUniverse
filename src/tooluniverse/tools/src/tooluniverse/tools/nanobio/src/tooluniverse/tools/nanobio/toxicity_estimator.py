"""
NanoBio Toxicity Estimator Tool

Author: Ghassan Muammar
Affiliation: Experts Group FZE
License: Apache-2.0

Early-stage in-silico toxicity estimation for nanoparticles based on
size (nm), surface charge (mV), and core material. Intended for
research and preclinical screening only (non-clinical use).
"""

from tooluniverse.tool_registry import register_tool
from tooluniverse.base_tool import BaseTool


@register_tool(
    "NanoBioToxicityEstimator",
    config={
        "name": "nanobio_toxicity_estimator",
        "type": "NanoBioToxicityEstimator",
        "description": (
            "Estimates early-stage nanoparticle toxicity risk using particle "
            "size (nm), surface charge (mV), and material composition. "
            "Designed for nanomedicine research and preclinical screening."
        ),
        "parameter": {
            "type": "object",
            "properties": {
                "size_nm": {"type": "number", "description": "Nanoparticle diameter in nm"},
                "charge_mV": {"type": "number", "description": "Surface zeta potential in mV"},
                "material": {"type": "string", "description": "Core material (e.g., lipid, polymer, gold)"}
            },
            "required": ["size_nm", "charge_mV", "material"]
        }
    }
)
class NanoBioToxicityEstimator(BaseTool):
    def run(self, arguments=None, **kwargs):
        if arguments is None:
            arguments = kwargs

        size_nm = float(arguments["size_nm"])
        charge_mV = float(arguments["charge_mV"])
        material = str(arguments["material"]).strip().lower()

        score = 0.0
        reasons = []

        if size_nm < 50:
            score += 2.5
            reasons.append("size < 50 nm")
        elif size_nm > 200:
            score += 3.0
            reasons.append("size > 200 nm")

        if abs(charge_mV) > 30:
            score += 2.5
            reasons.append("|charge| > 30 mV")

        if material in ["gold", "silver"]:
            score += 2.0
            reasons.append(f"material = {material}")

        score = max(0.0, min(score, 10.0))

        risk = "Low" if score < 3 else ("Medium" if score < 6 else "High")

        return {
            "toxicity_score": round(score, 2),
            "risk_level": risk,
            "reasons": reasons,
            "confidence": 0.5,
            "success": True
        }

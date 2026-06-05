# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 19:52:00 2026

@author: Jeffrey
"""

import streamlit as st

modules = {}

core_modules = {
    "Mechanics": {
        "module_weight": 0.25,
        "components": {
            "Mechanics exam": {"weight": 0.70, "max_mark": 100, "step": 1},
            "Mechanics APS 1": {"weight": 0.04, "max_mark": 10, "step": 1},
            "Mechanics APS 2": {"weight": 0.04, "max_mark": 10, "step": 1},
            "Relativity APS 1": {"weight": 0.06, "max_mark": 10, "step": 1},
            "Relativity APS 2": {"weight": 0.06, "max_mark": 10, "step": 1},
            "Relativity MCQ": {"weight": 0.005, "max_mark": 1, "step": 1},
            "Term 1 Seminars": {"weight": 0.05, "max_mark": 5, "step": 1},
            "Term 3 Seminars": {"weight": 0.02, "max_mark": 2, "step": 1},
            "Term 1 TATP": {"weight": 0.02, "max_mark": 2, "step": 1},
            "Term 3 TATP": {"weight": 0.005, "max_mark": 2, "step": 1},
        }
    },
    "Oscillations and Waves": {
        "module_weight": 0.25,
        "components": {
            "O&W Exam": {"weight": 0.70, "max_mark": 100, "step": 1},
            "O&W APS 1": {"weight": 0.0375, "max_mark": 10, "step": 1},
            "O&W APS 2": {"weight": 0.0375, "max_mark": 10, "step": 1},
            "O&W APS 3": {"weight": 0.0375, "max_mark": 10, "step": 1},
            "O&W APS 4": {"weight": 0.0375, "max_mark": 10, "step": 1},
            "Seminars": {"weight": 0.10, "max_mark": 10, "step": 1},
            "TATP": {"weight": 0.05, "max_mark": 5, "step": 1},
        }
    },
    "Vector Fields, Electricity and Magnetism": {
        "module_weight": 0.125,
        "components": {
            "VFEM Exam": {"weight": 0.80, "max_mark": 100, "step": 1},
            "VFEM APS 1": {"weight": 0.06, "max_mark": 10, "step": 1},
            "VFEM APS 2": {"weight": 0.06, "max_mark": 11, "step": 1},
            "Peerwise": {"weight": 0.08, "max_mark": 8, "step": 0.1},
        }
    },
    "Practical Physics": {
        "module_weight": 1/6,
        "components": {
            "Computing Project": {"weight": 0.10, "max_mark": 1, "step": 1},
            "Lab Report 1": {"weight": 0.15, "max_mark": 100, "step": 1},
            "Lab Report 2": {"weight": 0.15, "max_mark": 100, "step": 1},
            "Continuous Assessment": {"weight": 0.30, "max_mark": 100, "step": 0.1},
            "Problem Solving Test": {"weight": 0.30, "max_mark": 100, "step": 2},
        }
    },
    "Statistics of Measurement and Summer Project": {
        "module_weight": 0.125,
        "components": {
            "Seminars": {"weight": 0.03, "max_mark": 2, "step": 1},
            "Statistics Quiz": {"weight": 0.27, "max_mark": 100, "step": 1},
            "Summer Project": {"weight": 0.70, "max_mark": 100, "step": 1},
        }
    }
}

elective_modules = {
    "Elective Module":{
        "Advanced Electronics": {
            "module_weight": 1/12,
            "components": {
                "Quiz 1": {"weight": 0.15, "max_mark": 8, "step": 1},
                "Quiz 2": {"weight": 0.15, "max_mark": 8, "step": 1},
                "Quiz 3": {"weight": 0.15, "max_mark": 8, "step": 1},
                "Report": {"weight": 0.85, "max_mark": 130, "step": 1}
                }
            },
        "Maths Analysis": {
            "module_weight": 1/12,
            "components": {
                "Exam": {"weight": 1.00, "max_mark": 100, "step": 1}
                }
            }
        }
     }


def classify_grade(mark):
    if mark >= 70:
        return "First"
    elif mark >= 60:
        return "2:1"
    elif mark >= 50:
        return "2:2"
    elif mark >= 40:
        return "Third"
    else:
        return "Retake needed"

def raw_to_percentage(score, max_mark):
    return (score / max_mark) * 100 if max_mark > 0 else 0

st.title("First Year Physics Grade Predictor")

overall_mark = 0
module_results = {}

selected_elective = st.selectbox(
    "Choose your elective module:",
    list(elective_modules["Elective Module"].keys())
)

modules.update(core_modules)
modules[selected_elective] = elective_modules["Elective Module"][selected_elective]
    
for module_name, module_info in modules.items():
    st.subheader(f"{module_name} ({module_info['module_weight'] * 100:.1f}% of the year)")

    module_mark = 0

    for component_name, component_info in module_info["components"].items():
        weight = component_info["weight"]
        max_mark = component_info["max_mark"]
        step = component_info["step"]

        default_value = 0.7 * max_mark

        score = st.slider(
            f"{component_name} ({weight * 100:.1f}% of the module, out of {max_mark})",
            min_value=0.0,
            max_value=float(max_mark),
            value=float(default_value),
            step=float(step),
            key=f"{module_name}_{component_name}"
        )

        percentage_score = raw_to_percentage(score, max_mark)
        module_mark += percentage_score * weight

    module_results[module_name] = module_mark
    overall_mark += module_mark * module_info["module_weight"]

    st.write(f"Module mark: {module_mark:.2f}%")
    st.divider()


st.header("Results")

for module_name, module_mark in module_results.items():
    st.write(f"**{module_name}:** {module_mark:.2f}%")

st.metric("Overall Year Mark", f"{overall_mark:.2f}%")
st.write(f"**Classification:** {classify_grade(overall_mark)}")

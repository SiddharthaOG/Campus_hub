#!/usr/bin/env python
"""
Database seeding script for Campus Resource Hub.
Run with: python seed_data.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_hub.settings')
django.setup()

from resources.models import Resource

RESOURCES = [
    {
        "title": "Data Structures & Algorithms Notes",
        "description": "Comprehensive notes covering arrays, linked lists, trees, graphs, sorting algorithms, and dynamic programming. Includes time/space complexity analysis.",
        "subject": "CSE",
        "semester": 3,
        "branch": "CSE",
        "resource_type": "Notes",
        "tags": "algorithms, data-structures, python, interview-prep",
        "external_url": "https://example.com/resources/dsa-notes",
        "upvotes": 42,
        "download_count": 156,
    },
    {
        "title": "Operating Systems PYQs (2019-2023)",
        "description": "Previous year question papers for Operating Systems with solutions. Covers processes, scheduling, memory management, file systems, and deadlocks.",
        "subject": "CSE",
        "semester": 4,
        "branch": "CSE",
        "resource_type": "Previous Year Question Paper",
        "tags": "os, operating-systems, pyq, exam-prep",
        "external_url": "https://example.com/resources/os-pyqs",
        "upvotes": 67,
        "download_count": 234,
    },
    {
        "title": "Computer Networks Lab Manual",
        "description": "Complete lab manual for Computer Networks practical sessions. Includes socket programming, wireshark analysis, and network simulation exercises.",
        "subject": "CSE",
        "semester": 5,
        "branch": "CSE",
        "resource_type": "Lab Manual",
        "tags": "networks, socket-programming, wireshark, tcp-ip",
        "external_url": "https://example.com/resources/cn-lab-manual",
        "upvotes": 23,
        "download_count": 89,
    },
    {
        "title": "Database Management Systems Notes",
        "description": "Detailed notes on ER modeling, normalization, SQL, transactions, indexing, and query optimization. Includes practice problems.",
        "subject": "CSE",
        "semester": 4,
        "branch": "CSE",
        "resource_type": "Notes",
        "tags": "dbms, sql, normalization, transactions",
        "external_url": "https://example.com/resources/dbms-notes",
        "upvotes": 54,
        "download_count": 178,
    },
    {
        "title": "Digital Electronics PYQs",
        "description": "Collection of previous year questions for Digital Electronics. Covers logic gates, K-maps, flip-flops, counters, and state machines.",
        "subject": "ECE",
        "semester": 2,
        "branch": "ECE",
        "resource_type": "Previous Year Question Paper",
        "tags": "digital-electronics, logic-design, verilog, pyq",
        "external_url": "https://example.com/resources/de-pyqs",
        "upvotes": 31,
        "download_count": 112,
    },
    {
        "title": "Signals and Systems Notes",
        "description": "Complete notes on continuous/discrete signals, Fourier series, Laplace/Z transforms, sampling theorem, and LTI systems.",
        "subject": "ECE",
        "semester": 3,
        "branch": "ECE",
        "resource_type": "Notes",
        "tags": "signals, systems, fourier, laplace, dsp",
        "external_url": "https://example.com/resources/sas-notes",
        "upvotes": 38,
        "download_count": 145,
    },
    {
        "title": "Microcontrollers Lab Manual (8051/ARM)",
        "description": "Lab manual for microcontroller programming. Includes GPIO, timers, interrupts, UART, I2C, SPI interfacing with sensors.",
        "subject": "ECE",
        "semester": 5,
        "branch": "ECE",
        "resource_type": "Lab Manual",
        "tags": "microcontrollers, 8051, arm, embedded-c, iot",
        "external_url": "https://example.com/resources/mc-lab-manual",
        "upvotes": 29,
        "download_count": 98,
    },
    {
        "title": "Control Systems Study Material",
        "description": "Comprehensive study material covering transfer functions, stability analysis, root locus, Bode plots, and PID controller design.",
        "subject": "ECE",
        "semester": 4,
        "branch": "ECE",
        "resource_type": "Study Material",
        "tags": "control-systems, stability, pid, bode-plot",
        "external_url": "https://example.com/resources/cs-study-material",
        "upvotes": 19,
        "download_count": 76,
    },
    {
        "title": "Engineering Mathematics III Notes",
        "description": "Notes on complex analysis, Fourier series, partial differential equations, and probability distributions for engineering.",
        "subject": "Math",
        "semester": 3,
        "branch": "CSE",
        "resource_type": "Notes",
        "tags": "mathematics, complex-analysis, pde, probability",
        "external_url": "https://example.com/resources/math3-notes",
        "upvotes": 45,
        "download_count": 167,
    },
    {
        "title": "Discrete Mathematics PYQs",
        "description": "Previous year questions for Discrete Mathematics. Covers set theory, logic, graph theory, combinatorics, and recurrence relations.",
        "subject": "Math",
        "semester": 2,
        "branch": "CSE",
        "resource_type": "Previous Year Question Paper",
        "tags": "discrete-math, graph-theory, combinatorics, logic",
        "external_url": "https://example.com/resources/dm-pyqs",
        "upvotes": 33,
        "download_count": 121,
    },
    {
        "title": "Linear Algebra Reference Material",
        "description": "Quick reference for vector spaces, eigenvalues/eigenvectors, matrix decompositions (SVD, QR), and applications in ML.",
        "subject": "Math",
        "semester": 1,
        "branch": "AIDS",
        "resource_type": "Reference Material",
        "tags": "linear-algebra, eigenvalues, svd, machine-learning",
        "external_url": "https://example.com/resources/la-reference",
        "upvotes": 28,
        "download_count": 94,
    },
    {
        "title": "Quantum Mechanics Notes",
        "description": "Introduction to quantum mechanics: wave functions, Schrödinger equation, operators, hydrogen atom, and perturbation theory.",
        "subject": "Physics",
        "semester": 5,
        "branch": "CSQC",
        "resource_type": "Notes",
        "tags": "quantum-mechanics, schrodinger, wave-function, physics",
        "external_url": "https://example.com/resources/qm-notes",
        "upvotes": 21,
        "download_count": 67,
    },
    {
        "title": "Electromagnetic Theory PYQs",
        "description": "Previous year questions for Electromagnetic Theory. Covers electrostatics, magnetostatics, Maxwell's equations, and wave propagation.",
        "subject": "Physics",
        "semester": 3,
        "branch": "ECE",
        "resource_type": "Previous Year Question Paper",
        "tags": "electromagnetics, maxwell, electrostatics, waves",
        "external_url": "https://example.com/resources/emt-pyqs",
        "upvotes": 26,
        "download_count": 83,
    },
    {
        "title": "Physics Lab Manual (Optics & Modern Physics)",
        "description": "Lab manual for optics experiments (interference, diffraction, polarization) and modern physics (photoelectric effect, e/m ratio).",
        "subject": "Physics",
        "semester": 2,
        "branch": "ECE",
        "resource_type": "Lab Manual",
        "tags": "optics, diffraction, polarization, modern-physics",
        "external_url": "https://example.com/resources/physics-lab-manual",
        "upvotes": 15,
        "download_count": 54,
    },
    {
        "title": "Machine Learning Study Material",
        "description": "Curated study material for ML: supervised/unsupervised learning, neural networks, CNNs, transformers, and MLOps basics.",
        "subject": "CSE",
        "semester": 6,
        "branch": "AIE",
        "resource_type": "Study Material",
        "tags": "machine-learning, deep-learning, pytorch, tensorflow",
        "external_url": "https://example.com/resources/ml-study-material",
        "upvotes": 89,
        "download_count": 312,
    },
]


def seed():
    print("Clearing existing resources...")
    Resource.objects.all().delete()

    print(f"Creating {len(RESOURCES)} resources...")
    for data in RESOURCES:
        Resource.objects.create(**data)

    print("Database seeded successfully!")
    print(f"Total resources: {Resource.objects.count()}")


if __name__ == "__main__":
    seed()
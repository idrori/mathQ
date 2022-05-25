This folder contains json files representing every question evaluated in this paper and displayed in the Supplementary Materials Sections A-M. The files are organized by directories named after the question sources (course codes or MATH). Each json contains information relevant to one course question and the evaluations performed on it. The jsons contain the following fields:

| Field | Description |
| ----- | ----------- |
| "Course" | The text name of the course or dataset the question comes from |
| "Topic" | The topic from the course that the question targets |
| "Original question" | The original question text as presented from the source |
| "Codex input" | The text input into Codex that produces the correct solution (or code that evaluates to the correct solution) when run |
| "Codex code" | The code output that Codex generates when the Codex input is run |
| "Codex code explanation" | Step-by-step text explanation of the Codex code |
| "Program solution" | The solution to the question (equivalently, the output to the Codex code). If the question requires a graph output, this field will be the path to the image produced by the Codex code |
| "Solution type" | Either "Automatic Zero-shot", "Automatic Few-shot", or "Manual". A parentheses with a number following an "Automatic Few-shot" entry represents the number of question-code pairs used as examples (e.g. "Automatic Few-shot (2)"). The image below illustrates the process used to solve each question (by the end, every question is successfully solved).
| "GPT-3 response" | The output of evaluating the original question using the GPT-3 text-davinci-002 engine |
| "GPT-3 evaluation" | "Correct" if the GPT-3 response matches the program solution, "Incorrect" elsewise |


Diagram illustrating the zero-shot, then few-shot if unsuccessful, and if still unsuccessful, manual modification steps taken to solve each question.
![image](https://user-images.githubusercontent.com/51934413/170346165-98313e1c-f169-465a-abee-fd2b867b3a7f.png)


Seven university courses and six topics from the MATH dataset were considered. The courses and MATH topics included and their descriptions are as follows:

| Course Name | Description |
| ----------- | ----------- |
| MIT 6.042: Mathematics for Computer Science | Elementary discrete mathematics for science and engineering, with a focus on mathematical tools and proof techniques useful in computer science. Topics include logical notation, sets, relations, elementary graph theory, state machines and invariants, induction and proofs by contradiction, recurrences, asymptotic notation, elementary analysis of algorithms, elementary number theory and cryptography, permutations and combinations, counting tools, and discrete probability. |
| MIT 18.01: Single Variable Calculus | Differentiation and integration of functions of one variable, with applications. Informal treatment of limits and continuity. Differentiation: definition, rules, application to graphing, rates, approximations, and extremum problems. Indefinite integration; separable first-order differential equations. Definite integral; fundamental theorem of calculus. Applications of integration to geometry and science. Elementary functions. Techniques of integration. Polar coordinates. L'Hopital's rule. Improper integrals. Infinite series: geometric, p-harmonic, simple comparison tests, power series for some elementary functions. |
| MIT 18.02: Multivariable Calculus | Calculus of several variables. Vector algebra in 3-space, determinants, matrices. Vector-valued functions of one variable, space motion. Scalar functions of several variables: partial differentiation, gradient, optimization techniques. Double integrals and line integrals in the plane; exact differentials and conservative fields; Green's theorem and applications, triple integrals, line and surface integrals in space, Divergence theorem, Stokes' theorem; applications. |
| MIT 18.03: Differential Equations | Study of differential equations, including modeling physical systems. Solution of first-order ODEs by analytical, graphical, and numerical methods. Linear ODEs with constant coefficients. Complex numbers and exponentials. Inhomogeneous equations: polynomial, sinusoidal, and exponential inputs. Oscillations, damping, resonance. Fourier series. Matrices, eigenvalues, eigenvectors, diagonalization. First order linear systems: normal modes, matrix exponentials, variation of parameters. Heat equation, wave equation. Nonlinear autonomous systems: critical point analysis, phase plane diagrams. |
| MIT 18.05: Introduction to Probability and Statistics | Elementary introduction with applications. Basic probability models. Combinatorics. Random variables. Discrete and continuous probability distributions. Statistical estimation and testing. Confidence intervals. Introduction to linear regression. |
| MIT 18.06: Introduction to Linear Algebra | Basic subject on matrix theory and linear algebra, emphasizing topics useful in other disciplines, including systems of equations, vector spaces, determinants, eigenvalues, singular value decomposition, and positive definite matrices. Applications to least-squares approximations, stability of differential equations, networks, Fourier transforms, and Markov processes. Uses linear algebra software. Compared with 18.700, more emphasis on matrix algorithms and many applications. |
| Columbia University COMS3251: Computational Linear Algebra | Functions and compositions. Vectors and linear functions, matrices and linear transforms, inverses and Gaussian elimination. Vector spaces, bases, subspaces, and dimension. Inner products, norms, and orthogonal projections. Eigenvectors and eigenvalues, spectral decomposition. Quadratic forms, and singular value decomposition. |

| MATH Topic | Description |
| ----- | ----------- |
| Algebra | Algebra problems cover topics including exponents and logarithms, simplifying expressions, the coordinate plane, functions and their graphs, and quadratic functions and equations. |
| Counting and Probability | Counting \& probability cover multiple methods of counting (such as constructive and complementary counting) as well as probability questions that involve factorials, binomial coefficients, and the Binomial Theorem. | 
| Intermediate Algebra | Intermediate algebra problems cover more advanced algebraic topics, including advanced equations, polynomial roots, polynomial division, conic sections, sequences, and series. |
| Number Theory | Number theory problems cover topics including primes and divisibility, prime factorization, greatest common divisors and least common multiples, sum and product of divisors, numbers in different bases, and modular arithmetic. |
| Prealgebra | Prealgebra problems cover a basic topics from a variety of subjects within math. These include concepts of mean, median, and mode, primes and divisibility, working with fractions, decimals, and ratios, solving simple equations and inequalities, and simple counting problems. | 
| Precalculus | Precalculus covers topics such as vectors, matrices, trigonometric functions, trigonometric expressions, and complex numbers. |

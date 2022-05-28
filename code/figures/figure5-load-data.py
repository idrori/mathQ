import sys
import pandas

def main():
    f = sys.argv[1]
    d = pandas.read_csv(f)
    d.columns = ["Course", "Code"]

    counts = {}
    for _, course_code in d.iterrows():
        course, code = course_code.tolist()
        counts.setdefault(course, {})
        ql = set()
        for l in code.split("\n"):
            s = l.strip().split(" ")
            if s[0] in ["import", "from"]:
                lib = s[1].split(".")[0].lower()
                counts[course].setdefault(lib, 0)
                if lib in ql: # Ignore multiple imports in one response (e.g. from sympy import a, from sympy import b, etc. should all together count as one)
                    continue
                else:
                    ql.add(lib)
                counts[course][lib] += 1

    libs = set()
    for k, v in counts.items():
        for k in v.keys():
            libs.add(k)

    header = ["Course Number"] + sorted(libs)
    values = [[k] + [v.get(lib, 0) for lib in header[1:]] for k, v in counts.items()]
    d_out = pandas.DataFrame(values, columns=header)
    d_out.to_csv("figure5-imports.csv")


if __name__ == "__main__":
    main()

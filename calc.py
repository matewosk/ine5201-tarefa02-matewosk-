import tkinter as tk
from tkinter import messagebox, ttk


def parse_number(value: str) -> float:
    return float(value.strip().replace(",", "."))


def filter_numeric_input(value: str) -> str:
    filtered = []
    decimal_found = False

    for character in value:
        if character in "0123456789":
            filtered.append(character)
        elif character in ",." and not decimal_found:
            filtered.append(character)
            decimal_found = True
        elif character == "-" and not filtered:
            filtered.append(character)

    return "".join(filtered)


def calculate(first: float, second: float, operation: str) -> float:
    if operation == "+":
        return first + second
    if operation == "-":
        return first - second
    if operation == "*":
        return first * second
    if operation == "/":
        return first / second
    raise ValueError(f"Operação inválida: {operation}")


def show_result(operation: str) -> None:
    try:
        first = parse_number(first_value.get())
        second = parse_number(second_value.get())
        result = calculate(first, second, operation)
        history_list.insert(tk.END, f"{first:g} {operation} {second:g} = {result:g}")
        history_list.yview(tk.END)
        first_value.set(f"{result:g}")
        result_value.set(f"Resultado: {result:g}")
    except ValueError:
        messagebox.showerror("Entrada inválida", "Erro: Expressão inválida.")
    except ZeroDivisionError:
        messagebox.showerror("Operação inválida", "Erro: Divisão por zero.")


window = tk.Tk()
window.title("Calculadora")
window.resizable(False, False)

frame = ttk.Frame(window, padding=12)
frame.grid()

first_value = tk.StringVar()
second_value = tk.StringVar()
result_value = tk.StringVar(value="Resultado:")
validate_numeric_input = (
    window.register(
        lambda value: filter_numeric_input(value) == value
    ),
    "%P",
)

ttk.Label(frame, text="Primeiro número:").grid(row=0, column=0, sticky="w", pady=4)
ttk.Entry(
    frame,
    textvariable=first_value,
    validate="key",
    validatecommand=validate_numeric_input,
).grid(row=0, column=1, columnspan=4, sticky="ew", pady=4)

ttk.Label(frame, text="Segundo número:").grid(row=1, column=0, sticky="w", pady=4)
ttk.Entry(
    frame,
    textvariable=second_value,
    validate="key",
    validatecommand=validate_numeric_input,
).grid(row=1, column=1, columnspan=4, sticky="ew", pady=4)

for column, (label, operation) in enumerate(
    [("Somar", "+"), ("Subtrair", "-"), ("Multiplicar", "*"), ("Dividir", "/")],
    start=1,
):
    ttk.Button(
        frame,
        text=label,
        command=lambda operation=operation: show_result(operation),
    ).grid(row=2, column=column, padx=2, pady=8)

ttk.Label(frame, textvariable=result_value).grid(
    row=3, column=0, columnspan=5, sticky="w", pady=4
)

history_frame = ttk.LabelFrame(frame, text="Histórico", padding=8)
history_frame.grid(row=0, column=5, rowspan=4, padx=(16, 0), sticky="ns")

history_list = tk.Listbox(history_frame, height=10, width=28)
history_list.grid(row=0, column=0, sticky="nsew")

history_scrollbar = ttk.Scrollbar(
    history_frame,
    orient="vertical",
    command=history_list.yview,
)
history_scrollbar.grid(row=0, column=1, sticky="ns")
history_list.configure(yscrollcommand=history_scrollbar.set)

window.mainloop()

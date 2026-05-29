import math
from flask import render_template, request

def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]

    # Operações que usam apenas o primeiro número ou possuem lógica própria
    if operacao == "sqrt":
        if num1 < 0:
            return render_template("calculadora.html", etapas=f"Não existe raiz real de {num1}.", resultados="Erro: número negativo")
        resultado = math.sqrt(num1)
        return render_template("calculadora.html", etapas=f"√{num1} = {resultado}", resultados=resultado)

    elif operacao == "log":
        if num1 <= 0:
            return render_template("calculadora.html", etapas=f"Logaritmo exige número maior que zero. Base não pode ser aplicada a {num1}.", resultados="Erro: valor inválido")
        # Usando base 10 por padrão para simplificar
        resultado = math.log10(num1)
        return render_template("calculadora.html", etapas=f"log₁₀({num1}) = {resultado}", resultados=resultado)

    elif operacao == "bhaskara":
        # Para Bhaskara, usaremos num1 como 'a'. Capturamos os campos b e c do formulário estendido.
        b_valor = request.form.get("num2", "").strip()
        c_valor = request.form.get("num3", "").strip()
        
        if not b_valor or not c_valor:
            return render_template("calculadora.html", etapas="Para Bhaskara, informe os coeficientes B e C.", resultados="Erro")
        
        a = num1
        b = float(b_valor)
        c = float(c_valor)
        
        if a == 0:
            return render_template("calculadora.html", etapas="O coeficiente 'A' não pode ser zero em uma equação de 2º grau.", resultados="Erro")
        
        delta = (b ** 2) - (4 * a * c)
        
        if delta < 0:
            etapas = f"Δ = {b}² - 4·({a})·({c}) = {delta}"
            return render_template("calculadora.html", etapas=etapas, resultados="Sem raízes reais (Δ < 0)")
        
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        etapas = f"Δ = {delta} | x = ({-b} ± √{delta}) / {2*a}"
        resultados = f"x₁ = {x1} e x₂ = {x2}"
        return render_template("calculadora.html", etapas=etapas, resultados=resultados)

    # Operações que obrigatoriamente precisam de num2 tradicional
    num2_valor = request.form.get("num2", "").strip()
    if not num2_valor:
        return render_template("calculadora.html", etapas="Informe o segundo número para esta operação.", resultados="")
    num2 = float(num2_valor)

    if operacao == "+":
        resultado = num1 + num2
        etapas = f"{num1} + {num2} = {resultado}"
    elif operacao == "-":
        resultado = num1 - num2
        etapas = f"{num1} - {num2} = {resultado}"
    elif operacao == "*":
        resultado = num1 * num2
        etapas = f"{num1} × {num2} = {resultado}"
    elif operacao == "/":
        if num2 == 0:
            return render_template("calculadora.html", etapas=f"Divisão por zero: {num1} / {num2}", resultados="Erro: divisão por zero")
        resultado = num1 / num2
        etapas = f"{num1} ÷ {num2} = {resultado}"
    elif operacao == "**":
        resultado = num1 ** num2
        etapas = f"{num1} ^ {num2} = {resultado}"
    else:
        return render_template("calculadora.html", etapas="Operação desconhecida.", resultados="")

    return render_template("calculadora.html", etapas=etapas, resultados=resultado)

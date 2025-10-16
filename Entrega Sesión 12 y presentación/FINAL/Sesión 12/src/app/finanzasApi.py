import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock(symbol="MSFT"):
    data = yf.download(symbol, period="1mo", interval="1d")
    return data.index, data["Close"]

def plot_stock(fechas, precios, symbol="MSFT"):
    fig, ax = plt.subplots()
    ax.plot(fechas, precios, marker="o")
    ax.set_title(f"Evolución de {symbol} (último mes)")
    ax.set_ylabel("Precio de cierre (USD)")
    ax.tick_params(axis="x", rotation=45)
    plt.show()

if __name__ == "__main__":
    f, p = fetch_stock("MSFT")
    plot_stock(f, p, "MSFT")
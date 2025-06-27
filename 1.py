import os

project_path = "btc-dashboard"

files = {
    "package.json": '''{
  "name": "btc-dashboard",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.4.2"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.3.2",
    "vite": "^4.3.9"
  }
}
''',
    "vite.config.js": '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',
});
''',
    "tailwind.config.js": '''export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
''',
    "postcss.config.js": '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
''',
    "index.html": '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>BTC Dashboard</title>
  </head>
  <body class="bg-zinc-900 text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''',
    "src/index.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;
''',
    "src/main.jsx": '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import BitcoinDashboard from './BitcoinDashboard';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BitcoinDashboard />
  </React.StrictMode>
);
''',
    "src/BitcoinDashboard.jsx": '''import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceDot,
} from "recharts";

const REFRESH_INTERVAL = 300000; // 5 min

const mockPriceData = Array.from({ length: 40 }, (_, i) => {
  const base = 65000;
  return {
    time: `T${i}`,
    price: base + Math.sin(i / 3) * 300,
    deltaBuy: 500 + Math.cos(i / 5) * 100,
    deltaSell: 400 + Math.sin(i / 4) * 80,
  };
});

export default function BitcoinDashboard() {
  const [loading, setLoading] = useState(false);
  const [priceData, setPriceData] = useState([]);
  const [divergencePoints, setDivergencePoints] = useState([]);

  const fetchData = async () => {
    setLoading(true);
    setTimeout(() => {
      setPriceData(mockPriceData);
      calculateDivergence(mockPriceData);
      setLoading(false);
    }, 800);
  };

  const calculateDivergence = (data) => {
    const divergences = [];
    for (let i = 1; i < data.length; i++) {
      const priceTrend = data[i].price - data[i - 1].price;
      const deltaTrend =
        data[i].deltaBuy -
        data[i].deltaSell -
        (data[i - 1].deltaBuy - data[i - 1].deltaSell);

      if (priceTrend < 0 && deltaTrend > 0) {
        divergences.push({ ...data[i], type: "bullish" });
      } else if (priceTrend > 0 && deltaTrend < 0) {
        divergences.push({ ...data[i], type: "bearish" });
      }
    }
    setDivergencePoints(divergences);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📊 Wykres cen BTC/USD z dywergencjami</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={priceData}>
          <XAxis dataKey="time" />
          <YAxis
            domain={[
              (dataMin) => dataMin * 0.98,
              (dataMax) => dataMax * 1.02,
            ]}
          />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#fec106"
            strokeWidth={2}
            dot={false}
            name="Cena BTC/USD"
          />
          <Line
            type="monotone"
            dataKey={(d) => d.deltaBuy - d.deltaSell}
            stroke="#00ffaa"
            strokeWidth={1}
            dot={false}
            name="Delta (Kupno - Sprzedaż)"
          />
          {divergencePoints.map((d, idx) => (
            <ReferenceDot
              key={idx}
              x={d.time}
              y={d.price}
              r={5}
              fill={d.type === "bullish" ? "lime" : "red"}
              stroke="black"
              strokeWidth={1}
              label={d.type === "bullish" ? "📈" : "📉"}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <button
        className="mt-4 px-4 py-2 bg-gray-800 rounded text-white hover:bg-gray-700"
        onClick={fetchData}
        disabled={loading}
      >
        {loading ? "Ładowanie..." : "🔄 Odśwież dane"}
      </button>
    </div>
  );
}
''',
    "README.md": '''# Kompendium Tradera – BTC Dashboard

Prosty dashboard do analizy rynku BTC/USD w czasie rzeczywistym:

- Wykres cen BTC/USD z linią delta (kupno - sprzedaż)
- Wykrywanie dywergencji byczych i niedźwiedzich
- Auto-odświeżanie danych co 5 minut
- Symulowane dane testowe (działa bez API)
- Gotowy do hostowania na Vercel

## Technologie

- React (Vite)
- TailwindCSS
- Recharts (do wykresów)

## Uruchomienie lokalne

1. Zainstaluj zależności:
   ```bash
   npm install

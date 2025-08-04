// src/App.jsx
import React from 'react';
import { RefreshCcw, AlertCircle} from 'lucide-react';

import { useData } from './hooks/useData';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import MetricsSection from './components/metrics/MetricsSection';
import PriceChart from './components/charts/PriceChart';
import ReturnsChart from './components/charts/ReturnsChart';
import EventsSection from './components/events/EventsSection';
import './index.css';

export default function App() {
  const { data, loading, error, fetchData } = useData();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 font-inter">
        <RefreshCcw className="animate-spin text-blue-500 mb-4" size={48} />
        <p className="text-xl text-gray-700 font-semibold">
          Running Bayesian analysis... This may take a moment.
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-red-50 text-red-700 font-inter">
        <AlertCircle size={48} className="mb-4" />
        <p className="text-xl font-bold">Error Loading Data</p>
        <p className="text-center mt-2 px-4">{error}</p>
        <button
          onClick={fetchData}
          className="mt-6 px-6 py-2 bg-red-500 text-white rounded-full font-bold shadow hover:bg-red-600 transition"
        >
          Try Again
        </button>
      </div>
    );
  }

  const { prices_raw, preprocessed_data, model_results, relevant_events } = data;

  return (
    <div className="bg-gray-50 min-h-screen flex flex-col font-inter">
      <style>
        {`
        @import url('https://rsms.me/inter/inter.css');
        .font-inter { font-family: 'Inter', sans-serif; }
        .recharts-wrapper { overflow: visible !important; }
        .recharts-tooltip-cursor {
          fill: rgba(0,0,0,0.05);
        }
        `}
      </style>
      <script src="https://cdn.tailwindcss.com"></script>
      <Header />
      <main className="flex-grow px-4 md:px-8 lg:px-16 py-8">
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Brent Oil Change Point Dashboard
          </h1>
          <p className="text-gray-600">
            Analyzing historical Brent oil prices to detect structural breaks
            using a Bayesian Change Point model.
          </p>
        </div>
        
        {data && (
          <>
            <MetricsSection modelResults={model_results} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 my-8 px-4 md:px-8 lg:px-16">
              <PriceChart data={prices_raw} changePointDate={model_results.change_point_date} />
              <ReturnsChart data={preprocessed_data} changePointDate={model_results.change_point_date} />
            </div>
            <EventsSection events={relevant_events} changePointDate={model_results.change_point_date} />
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}



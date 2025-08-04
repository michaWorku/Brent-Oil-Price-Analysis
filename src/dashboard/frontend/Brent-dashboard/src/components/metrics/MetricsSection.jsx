// Displays key metrics from the model results.
import React from 'react';
import { TrendingUp, TrendingDown, Calendar } from 'lucide-react';

const MetricCard = ({ icon, label, value, description }) => (
  <div className="bg-white p-6 rounded-xl shadow-lg flex items-center space-x-4 h-full">
    <div className="p-3 bg-blue-100 rounded-full text-blue-600 flex-shrink-0">
      {icon}
    </div>
    <div className="flex-1">
      <h3 className="text-lg font-medium text-gray-500">{label}</h3>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
      <p className="text-sm text-gray-400 mt-1">{description}</p>
    </div>
  </div>
);

const MetricsSection = ({ modelResults }) => {
  if (!modelResults) return null;
  const { change_point_date, mu_1_post, mu_2_post, sigma_1_post, sigma_2_post } = modelResults;

  const muChangeIcon = mu_2_post > mu_1_post ? <TrendingUp size={24} /> : <TrendingDown size={24} />;
  const volatilityChangeDescription = `Volatility changed from ${sigma_1_post.toFixed(4)} to ${sigma_2_post.toFixed(4)}.`;

  return (
    <section className="p-4 md:p-8 lg:p-16 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Key Metrics</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          icon={<Calendar size={24} />}
          label="Change Point Date"
          value={change_point_date}
          description="The most probable date of the structural break."
        />
        <MetricCard
          icon={muChangeIcon}
          label="Pre-Change Mean"
          value={`${(mu_1_post * 100).toFixed(2)}%`}
          description="Average daily log return before the change."
        />
        <MetricCard
          icon={muChangeIcon}
          label="Post-Change Mean"
          value={`${(mu_2_post * 100).toFixed(2)}%`}
          description="Average daily log return after the change."
        />
        <MetricCard
          icon={sigma_2_post > sigma_1_post ? <TrendingUp size={24} /> : <TrendingDown size={24} />}
          label="Volatility Change"
          value={`${(sigma_2_post / sigma_1_post).toFixed(2)}x`}
          description={volatilityChangeDescription}
        />
      </div>
    </section>
  );
};

export default MetricsSection;
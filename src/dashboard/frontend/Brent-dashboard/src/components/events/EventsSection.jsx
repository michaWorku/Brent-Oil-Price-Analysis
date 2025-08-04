// Displays the list of relevant events around the change point.
import React from 'react';
import { AlertCircle, Calendar } from 'lucide-react';

const EventsSection = ({ events, changePointDate }) => {
  if (!events || events.length === 0) {
    return (
      <section className="bg-white rounded-xl shadow-lg p-6 mb-8 mt-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Relevant Events</h2>
        <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400 text-yellow-800 flex items-start space-x-3">
          <AlertCircle size={20} className="flex-shrink-0 mt-1" />
          <div>
            <p className="font-medium">Detected Change Point: {changePointDate}</p>
            <p className="text-sm">
              No significant events were found within 30 days of the detected change point.
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="p-4 md:p-8 lg:p-16 mt-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Relevant Events</h2>
      <div className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400 text-yellow-800 flex items-start space-x-3 mb-6">
        <AlertCircle size={20} className="flex-shrink-0 mt-1" />
        <div>
          <p className="font-medium">Detected Change Point: {changePointDate}</p>
          <p className="text-sm">
            Below are significant events that occurred within 30 days of the
            detected change point.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event, index) => (
          <div key={index} className="bg-white p-6 rounded-xl shadow-lg h-full flex flex-col justify-between">
            <div>
              <p className="text-lg font-bold text-gray-900">{event.Event_Name}</p>
              <p className="text-sm text-gray-500 mt-1 flex items-center space-x-2">
                <Calendar size={14} />
                <span>{event.Date}</span>
              </p>
              <p className="text-sm text-gray-700 mt-3">{event.Description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default EventsSection;

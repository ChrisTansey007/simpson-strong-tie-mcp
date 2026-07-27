import { useState } from 'react';

interface ReviewItem {
  id: string;
  modelNumber: string;
  claimType: string;
  candidateValue: string;
  unit: string;
  pageNumber: number;
  confidence: number;
  boundingBox: [number, number, number, number];
  status: 'AUTO_PARSED_REVIEW_REQUIRED' | 'HUMAN_VERIFIED' | 'REJECTED';
}

const INITIAL_QUEUE: ReviewItem[] = [
  {
    id: 'claim-101',
    modelNumber: 'H1A',
    claimType: 'allowable_uplift_load',
    candidateValue: '745',
    unit: 'lbf',
    pageNumber: 287,
    confidence: 0.94,
    boundingBox: [120, 450, 300, 480],
    status: 'AUTO_PARSED_REVIEW_REQUIRED',
  },
  {
    id: 'claim-102',
    modelNumber: 'LUS28',
    claimType: 'allowable_download_load',
    candidateValue: '1350',
    unit: 'lbf',
    pageNumber: 142,
    confidence: 0.91,
    boundingBox: [200, 320, 380, 360],
    status: 'AUTO_PARSED_REVIEW_REQUIRED',
  },
];

export default function ReviewQueue() {
  const [items, setItems] = useState<ReviewItem[]>(INITIAL_QUEUE);

  const handleDecision = (id: string, decision: 'HUMAN_VERIFIED' | 'REJECTED') => {
    setItems((prev) =>
      prev.map((item) => (item.id === id ? { ...item, status: decision } : item))
    );
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl mt-8">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Human Verification Review Queue</h2>
          <p className="text-xs text-slate-400">
            Verify AI-extracted candidate claims against catalog evidence crops before publishing to MCP tools.
          </p>
        </div>
        <span className="px-3 py-1 bg-amber-500/10 text-amber-400 text-xs font-semibold rounded-full border border-amber-500/20">
          {items.filter((i) => i.status === 'AUTO_PARSED_REVIEW_REQUIRED').length} Pending
        </span>
      </div>

      <div className="mt-4 divide-y divide-slate-800">
        {items.map((item) => (
          <div key={item.id} className="py-4 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span className="font-bold text-amber-500">{item.modelNumber}</span>
                <span className="text-xs text-slate-400">({item.claimType})</span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                  p. {item.pageNumber}
                </span>
              </div>
              <p className="text-sm text-slate-200 mt-1">
                Candidate Capacity: <strong className="text-emerald-400">{item.candidateValue} {item.unit}</strong>{' '}
                <span className="text-xs text-slate-500 font-mono">(Confidence: {(item.confidence * 100).toFixed(0)}%)</span>
              </p>
            </div>

            <div className="flex-1 w-full lg:w-auto">
              <div className="bg-slate-800/50 rounded p-3 border border-slate-700">
                <p className="text-xs text-slate-400 mb-2">Evidence Crop Bounding Box</p>
                <div className="flex flex-wrap items-center gap-3 font-mono text-xs text-slate-300 bg-slate-900 rounded p-2 border border-slate-800">
                  <span>x0: <span className="text-sky-400">{item.boundingBox[0]}</span></span>
                  <span>y0: <span className="text-sky-400">{item.boundingBox[1]}</span></span>
                  <span>x1: <span className="text-sky-400">{item.boundingBox[2]}</span></span>
                  <span>y1: <span className="text-sky-400">{item.boundingBox[3]}</span></span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2 w-full lg:w-auto justify-end">
              {item.status === 'AUTO_PARSED_REVIEW_REQUIRED' ? (
                <>
                  <button
                    onClick={() => handleDecision(item.id, 'HUMAN_VERIFIED')}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded-lg transition whitespace-nowrap"
                  >
                    Approve Claim
                  </button>
                  <button
                    onClick={() => handleDecision(item.id, 'REJECTED')}
                    className="px-3 py-1.5 bg-rose-600/20 border border-rose-500/30 text-rose-400 hover:bg-rose-600/30 text-xs font-medium rounded-lg transition whitespace-nowrap"
                  >
                    Reject
                  </button>
                </>
              ) : (
                <span
                  className={`text-xs font-semibold uppercase px-2.5 py-1 rounded whitespace-nowrap ${
                    item.status === 'HUMAN_VERIFIED'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                  }`}
                >
                  {item.status}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

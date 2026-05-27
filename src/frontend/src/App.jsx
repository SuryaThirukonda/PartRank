import "./App.css";
import { useEffect, useMemo, useState } from "react";

const API_BASE = "http://localhost:8000/gpus/";
const PAGE_SIZE = 50;
const DEFAULT_FETCH_LIMIT = 9999;

function App() {
  const [gpus, setGpus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [maxPrice, setMaxPrice] = useState("");
  const [sortMode, setSortMode] = useState("performance");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedGpu, setSelectedGpu] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState(null);

  useEffect(() => {
    async function fetchGpus() {
      try {
        setLoading(true);
        setError(null);

        const params = new URLSearchParams({
          skip: "0",
          limit: String(DEFAULT_FETCH_LIMIT),
          Max_price: maxPrice === "" ? "999999" : String(maxPrice),
          Min_price: "0",
          search: "",
          Sort_by_Performance_desc: String(sortMode === "performance"),
          Sort_by_Performance_asc: "false",
          Sort_by_Pricetoperf_asc: String(sortMode === "value"),
          Sort_by_Pricetoperf_desc: "false",
          SortPriceAsc: String(sortMode === "price_asc"),
          SortPriceDesc: String(sortMode === "price_desc"),
        });

        const response = await fetch(`${API_BASE}?${params.toString()}`);

        if (!response.ok) {
          throw new Error(response.statusText);
        }

        const data = await response.json();
        setGpus(data);
        setCurrentPage(1);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchGpus();
  }, [maxPrice, sortMode]);

  const totalPages = useMemo(() => {
    return Math.max(1, Math.ceil(gpus.length / PAGE_SIZE));
  }, [gpus.length]);

  const safeCurrentPage = Math.min(currentPage, totalPages);
  const startIndex = (safeCurrentPage - 1) * PAGE_SIZE;
  const visibleGpus = gpus.slice(startIndex, startIndex + PAGE_SIZE);

  function getValueScore(gpu) {
    if (gpu.price === null || gpu.price === undefined) {
      return null;
    }

    if (gpu.price <= 0 || gpu.performance === null || gpu.performance === undefined) {
      return null;
    }

    return gpu.performance / gpu.price;
  }

  async function openGpuDetails(gpuId) {
    try {
      setDetailLoading(true);
      setDetailError(null);

      const response = await fetch(`${API_BASE}${gpuId}`);

      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const data = await response.json();
      setSelectedGpu(data);
    } catch (err) {
      console.error("Error fetching GPU details:", err);
      setDetailError(err.message);
    } finally {
      setDetailLoading(false);
    }
  }

  function handleSortChange(nextSortMode) {
    setSortMode(nextSortMode);
  }

  function handleMaxPriceChange(event) {
    const nextValue = event.target.value;
    setMaxPrice(nextValue === "" ? "" : Number(nextValue));
  }

  function formatPrice(price) {
    if (price === null || price === undefined) {
      return "N/A";
    }

    return `$${Number(price).toFixed(2)}`;
  }

  function formatFieldValue(key, value) {
    if (value === null || value === undefined) {
      return "N/A";
    }

    if (typeof value === "string" && key.toLowerCase().includes("created_at")) {
      return new Date(value).toLocaleString();
    }

    if (typeof value === "string" && key.toLowerCase().includes("updated_at")) {
      return new Date(value).toLocaleString();
    }

    if (key === "price") {
      return formatPrice(value);
    }

    if (key === "performance") {
      return String(value);
    }

    return String(value);
  }

  function renderDetailView() {
    if (detailLoading) {
      return <p>Loading GPU details...</p>;
    }

    if (detailError) {
      return <p className="error">Error: {detailError}</p>;
    }

    if (!selectedGpu) {
      return null;
    }

    const valueScore = getValueScore(selectedGpu);

    return (
      <section className="detail-view">
        <button
          type="button"
          className="back-button"
          onClick={() => setSelectedGpu(null)}
        >
          Back to results
        </button>

        <div className="detail-card">
          <div className="detail-header">
            <h2>{selectedGpu.name}</h2>
            <p className="detail-subtitle">
              Value score: {valueScore !== null ? valueScore.toFixed(2) : "N/A"}
            </p>
          </div>

          <dl className="detail-grid">
            {Object.entries(selectedGpu).map(([key, value]) => (
              <div className="detail-row" key={key}>
                <dt>{key}</dt>
                <dd>{formatFieldValue(key, value)}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>
    );
  }

  function renderListView() {
    if (loading) {
      return <p>Loading...</p>;
    }

    if (error) {
      return <p className="error">Error: {error}</p>;
    }

    if (gpus.length === 0) {
      return <p>No GPU data available.</p>;
    }

    return (
      <>
        <div className="toolbar">
          <div className="control-group">
            <label htmlFor="max-price">Max Price</label>
            <input
              id="max-price"
              type="number"
              min="0"
              step="1"
              value={maxPrice}
              onChange={handleMaxPriceChange}
              placeholder="Leave blank for all"
            />
          </div>

          <div className="sort-group">
            <button
              type="button"
              className={sortMode === "performance" ? "sort-button active" : "sort-button"}
              onClick={() => handleSortChange("performance")}
            >
              Performance
            </button>
            <button
              type="button"
              className={sortMode === "price_asc" ? "sort-button active" : "sort-button"}
              onClick={() => handleSortChange("price_asc")}
            >
              Price Low to High
            </button>
            <button
              type="button"
              className={sortMode === "price_desc" ? "sort-button active" : "sort-button"}
              onClick={() => handleSortChange("price_desc")}
            >
              Price High to Low
            </button>
            <button
              type="button"
              className={sortMode === "value" ? "sort-button active" : "sort-button"}
              onClick={() => handleSortChange("value")}
            >
              Value Score
            </button>
          </div>
        </div>

        <p className="results-meta">
          Showing {visibleGpus.length} of {gpus.length} GPUs on page {safeCurrentPage} of {totalPages}
        </p>

        <div className="card-list">
          {visibleGpus.map((gpu) => {
            const valueScore = getValueScore(gpu);

            return (
              <button
                type="button"
                className="gpu-card"
                key={gpu.id}
                onClick={() => openGpuDetails(gpu.id)}
              >
                <h2>{gpu.name}</h2>
                <p>Price: {formatPrice(gpu.price)}</p>
                <p>Performance: {gpu.performance}</p>
                <p>Value Score: {valueScore !== null ? valueScore.toFixed(2) : "N/A"}</p>
                <span className="card-hint">Click to view metadata</span>
              </button>
            );
          })}
        </div>

        <nav className="pagination" aria-label="GPU result pages">
          <button
            type="button"
            className="page-button"
            onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
            disabled={safeCurrentPage === 1}
          >
            Previous
          </button>

          {Array.from({ length: totalPages }, (_, index) => index + 1).map((page) => (
            <button
              type="button"
              key={page}
              className={page === safeCurrentPage ? "page-button active" : "page-button"}
              onClick={() => setCurrentPage(page)}
            >
              {page}
            </button>
          ))}

          <button
            type="button"
            className="page-button"
            onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
            disabled={safeCurrentPage === totalPages}
          >
            Next
          </button>
        </nav>
      </>
    );
  }

  return (
    <main className="page">
      <h1>PartRank</h1>
      <p>Browse GPUs by performance, price, and value.</p>

      {selectedGpu ? renderDetailView() : renderListView()}
    </main>
  );
}

export default App;

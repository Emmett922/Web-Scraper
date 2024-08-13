// Necessary import
import React, { useState, useEffect } from 'react'

function App() {
  // React state hooks to manage laptops data, loading status, and scraping status
  const [laptops, setLaptops] = useState([]); // Holds laptop data
  const [loading, setLoading] = useState(false); // Indicates if data is being loaded
  const [scraping, setScraping] = useState(false); // Indicates whether the scraper is running

  // Function to start the scraper
  const startScraper = async () => {
    try {
      setScraping(true); // Disable button and indicate that scraping is ongoing
      const response = await fetch("http://localhost:5000/start-scraper", { method: "POST" });
      if (response.ok) {
        console.log("Scraper started.");
        setLoading(true); // Show loading state while data is being fetched
        checkStatusAndFetch(); // Check scraper status and fetch the data
      } else {
        console.error("Failed to start scraper.");
      }
    } catch (err) {
      console.error("Error starting scraper:", err);
    } finally {
      setScraping(false); // Re-enable button after attempting to start the scraper
    }
  };

  // Function to periodically check the status of the scraper and fetch the data
  const checkStatusAndFetch = async () => {
    const fetchInterval = setInterval(async () => {
      try {
        const res = await fetch("http://localhost:5000/status");
        const status = await res.json();

        if (status.status === "idle") { // If the scraper is idle (finished)
          clearInterval(fetchInterval); // Stop checking the status
          setScraping(false);

          fetchLaptops(); // Fetch the scraped laptop data
        } else {
          setTimeout(checkStatusAndFetch, 2000); // Check status every 2 sec
        }
      } catch (err) {
        console.error("Error checking status or fetching data:", err);
        clearInterval(fetchInterval); // Stop checking status if an error occurs
        setLoading(false);
        setScraping(false);
      }
    }, 2000); // Set interval for status check to every 2 sec
  };

  // Function to fetch the scraped laptop data
  const fetchLaptops = async () => {
    try {
      const response = await fetch("http://localhost:5000/laptops")
      if (response.status === 202) {
        console.log("Data is not ready, still scraping...");
        setTimeout(fetchLaptops, 3000); // Retry in 3 sec
      } else if (response.status === 400) {
        console.error("Bad request to /laptops");
      } else {
        const data = await response.json();
        setLaptops(data.data || []); // Updata stat with the fetched laptop data
        setLoading(false); // Stop loading once data is fetched
      }
    } catch (err) {
      console.error("Error fetching laptops:", err);
    }
  };

  // Rendered UI
  return (
    <div>
      <button onClick={startScraper} disabled={scraping}>
        {scraping ? 'Starting Scraper...' : 'Start Scraper'} {/* Button text changes based on scraping status */}
      </button>
      {loading ? (
        <p>Loading Data...</p> // Show loading message while data is being fetched
      ) : (
        laptops.length > 0 ? (
          <table>
            <thread>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Price</th>
              </tr>
            </thread>
            <tbody>
              {laptops.map((laptop, i) => (
                <tr key={i}>
                  <td>{laptop.title}</td>
                  <td>
                    {laptop.descr.length > 60 ? ( // Truncate descr. if it's too long
                      <span>
                        {laptop.descr.slice(0, 60)}...
                        <span
                          style={{ color: 'blue', cursor: 'pointer' }}
                          onClick={() => alert(laptop.descr)} // Show full descr. on click
                        >
                          [Read more]
                        </span>
                      </span>
                    ) : (
                      laptop.descr
                    )}
                  </td>
                  <td>{laptop.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No laptops available</p> // Show if no laptop data is available
        )
      )}
    </div>
  )
}

export default App

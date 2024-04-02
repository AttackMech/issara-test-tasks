import React, { useState, useEffect, useCallback } from "react";

const DealerList = () => {
  const [initialLoad, setInitialLoad] = useState(false);
  const [addMore, setAddMore] = useState(true)
  const [dealers, setDealers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [cityFilter, setCityFilter] = useState("");
  const [nextLink, setNextLink] = useState("");

  const fetchData = (queryString) => {
    const fetchString = queryString ? queryString : createQueryString();

    fetch(fetchString)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        return response.json();
      })
      .then((data) => {
        if (addMore) {
        setDealers((prevDealers) => [...prevDealers, ...data["results"]]);
        } else {
            setDealers(data["results"])
        }
        setAddMore(true)
        setNextLink(data["next"]);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const handleScroll = useCallback(() => {
    if (
      nextLink &&
      window.innerHeight + document.documentElement.scrollTop >=
        document.documentElement.offsetHeight - 20
    ) {
      debouncedFetchData(nextLink);
    }
  }, [nextLink, fetchData]);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (initialLoad) {
        fetchData();
        
      } else {
        setInitialLoad(true);
      }
  }, [searchQuery, cityFilter, initialLoad]);

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [handleScroll]);

  const createQueryString = () => {
    let base = "http://127.0.0.1:8000/dealers/";

    if (searchQuery) {
      base = `${base}?search=${searchQuery}`;
    }

    if (cityFilter) {
      base = `${base}${searchQuery ? "&" : "?"}city=${cityFilter}`;
    }

    return base;
  };

  const debounce = (func, delay) => {
    let timeoutId;
    return function (...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
      }, delay);
    };
  };

  const debouncedFetchData = debounce(fetchData, 100);

  const handleNameSearch = (name) => {
    setAddMore(false)
    setSearchQuery(name)
  }

  const handleCityFilter = (city) => {
    setAddMore(false)
    setCityFilter(city)
  }

  const displayDealers = () => {
    if (!dealers || dealers.length === 0) {
      return <div>No results available. Adjust search.</div>;
    }

    return (
      <div className="dealer_list">
        {dealers.map((dealer) => {
          return (
            <div key={dealer.id} className="dealer">
              <span>{dealer.id}. </span>
              <span className="dealer_data">{dealer.name}</span>
              <ul>
                <li>
                  EN Name: <span className="dealer_data">{dealer.name_en}</span>
                </li>
                <li>
                  License #:{" "}
                  <span className="dealer_data">{dealer.license_number}</span>
                </li>
                <li>
                  Status: <span className="dealer_data">{dealer.status}</span>
                </li>
                <li>
                  Logo: <span className="dealer_data">{dealer.logo}</span>
                </li>
                <li>
                  Score:{" "}
                  <span className="dealer_data">{dealer.rating_score}</span>
                </li>
                <li>
                  Ratings:{" "}
                  <span className="dealer_data">{dealer.rating_count}</span>
                </li>
                <li>
                  Commenets:{" "}
                  <span className="dealer_data">{dealer.comments_count}</span>
                </li>
                <li>
                  Popularity:{" "}
                  <span className="dealer_data">{dealer.popularity}</span>
                </li>
                <li>
                  City: <span className="dealer_data">{dealer.city}</span>
                </li>
              </ul>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div>
      <div className="search_filter">
        <div>
          <label htmlFor="searchInput">Search by name:</label>
          <input
            id="searchInput"
            type="text"
            value={searchQuery}
            onChange={(e) => handleNameSearch(e.target.value)}
            placeholder="Search by name"
          />
        </div>
        <div>
          <label htmlFor="cityInput">Filter by city:</label>
          <input
            id="cityInput"
            type="text"
            value={cityFilter}
            onChange={(e) => handleCityFilter(e.target.value)}
            placeholder="Filter by city"
          />
        </div>
      </div>
      <div>{displayDealers()}</div>
    </div>
  );
};

export default DealerList;

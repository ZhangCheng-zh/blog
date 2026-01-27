
/* Coding test:
frontend:

# The Challenge: 

Data Consumption and Table View You are tasked with building a component to consume and display service status data for the Service Catalog frontend. 

### Data Model & Fetching Define a TypeScript interface (or type) to model the data returned from the public API: https://jsonplaceholder.typicode.com/todos. 

Hint: The key fields are id, title, and completed. Create a component (e.g., ServiceStatusTable). Fetch Data: Use a fetch or axios call within useEffect to retrieve the data from the public endpoint. 

### UI Implementation Table Rendering: Display the fetched data in a visually clear HTML table with three columns: Service ID (mapped from id) Service Name (mapped from title) Provisioning Status (mapped from completed): If completed is true, show the status as "Available". 

If completed is false, show the status as "In Progress". State Handling: Implement the following states using React hooks: Loading State: Show a simple "Loading services..." message while the data is being fetched. Error State: If the fetch fails, display a clear "Error loading data." message. 

## Verification Run the React app (e.g., npm start in the terminal). Verify the browser view shows the table with data correctly mapped and transformed.
*/

import React, { userEffect, useState } from 'react';

type TodoItem = {
    id: number;
    title: string;
    completed: boolean;
}

export default function ServiceStatusTable() {
    const [items, setItems] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [hasError, setHasError] = useState(false);

    userEffect(() => {
        let isCancelled = false;

        async function fetchData() {
            try {
                setIsLoading(true);
                setHasError(false);

                const resp = await fetch('https://jsonplaceholder.typicode.com/todos')
                if (!resp.ok) {
                    throw new Error(`HTTP ${resp.status}`)
                }

                const data = await resp.json();
                if (!isCancelled) {
                    setItems(data);
                }
            } catch {
                if (!isCancelled) {
                    setHasError(true);
                }
            } finally {
                if (!isCancelled) {
                    setIsLoading(false);
                }
            }
        }

        fetchData();

        return () => {
            isCancelled = true;
        }

    }, [])


    if (isLoading) {
        return <div>Loading services......</div>;
    }

    if (hasError) {
        return <div>Error loading data.</div>
    }

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Service ID</th>
                        <th>Service Name</th>
                        <th>Provisioning Status</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        items.map((it: TodoItem) => (
                            <tr key = {it.id}>
                                <td>{it.id}</td>
                                <td>{it.title}</td>
                                <td>{it.completed ? 'Available' : 'In Progress'}</td>
                            </tr>
                        ))
                    }
                </tbody>
            </table>
        </div>
    )
}

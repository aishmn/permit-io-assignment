import React, { useEffect, useState } from 'react';
import { fetchResourcesData, fetchRolesData } from './api/permitAPI';

import Loading from './components/Loading';
import Navbar from './components/Navbar';
import ResourceTree from './components/ResourceTree';
import RoleCard from './components/RoleCard';

interface Role {
  key: string;
  name: string;
  permissions: string[];
  description?: string;
}

interface Resource {
  key: string;
  id: string;
  name: string;
  actions: Record<string, any>;
  roles: Record<string, Role>;
}

const App: React.FC = () => {
  const [rolesData, setRolesData] = useState<Role[]>([]);
  const [resourcesData, setResourcesData] = useState<Resource[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [roles, resources] = await Promise.all([
          fetchRolesData(),
          fetchResourcesData(),
        ]);
        setRolesData(roles);
        setResourcesData(resources);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const renderError = () => (
    <div className="text-red-500 text-center">
      <p>{error}</p>
    </div>
  );

  const renderLoading = () => <Loading />;

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <Navbar />
      <div className="container mx-auto">
        {loading ? (
          renderLoading()
        ) : error ? (
          renderError()
        ) : (
          <>
            <RoleCard rolesData={rolesData} />
            <ResourceTree resourcesData={resourcesData} />
          </>
        )}
      </div>
    </div>
  );
};

export default App;

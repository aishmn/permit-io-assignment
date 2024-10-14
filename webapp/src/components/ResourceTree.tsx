import PropTypes from 'prop-types';
import React from 'react';

interface Action {
  key: string;
  name: string;
  description?: string;
}

interface Role {
  key: string;
  name: string;
  permissions: string[];
}

interface Resource {
  key: string;
  id: string;
  name: string;
  actions: Record<string, Action>;
  roles: Record<string, Role>;
}

interface ResourceTreeProps {
  resourcesData: Resource[];
}

const ResourceTree: React.FC<ResourceTreeProps> = ({ resourcesData }) => {
  if (resourcesData.length === 0)
    return (
      <div className="text-red-500 text-center">
        <p>No resources available.</p>
        <p>Try creating a new resource!</p>
      </div>
    );

  return (
    <div className="p-6 bg-gray-100 rounded-lg shadow-lg">
      <h2 className="mb-4 text-3xl font-bold text-gray-800 text-left">
        Resource Relationship Tree
      </h2>
      <div className="space-y-6 capitalize">
        {resourcesData.map(resource => (
          <div
            key={resource.id}
            className="bg-white rounded-lg shadow-md p-4 transition-transform transform hover:scale-99 cursor-pointer"
            role="region"
            aria-labelledby={`resource-${resource.id}`}>
            <h3
              className="text-2xl font-semibold text-gray-900"
              id={`resource-${resource.id}`}>
              {resource.name}
            </h3>
            <div className="mt-4">
              <h4 className="font-semibold text-gray-800 border-b border-gray-300 pb-2">
                Available Actions
              </h4>
              <ul className="flex flex-col space-y-3 mt-2 bg-stone-200 shadow-sm rounded-sm px-3 py-4">
                {Object.values(resource.actions).map(action => (
                  <li
                    key={action.key}
                    className="text-stone-800 uppercase text-sm">
                    {action.name}
                  </li>
                ))}
              </ul>
            </div>
            <div className="mt-4">
              <h4 className="font-semibold text-gray-800 border-b border-gray-300 pb-2">
                Roles and Permissions
              </h4>
              <ul className="space-y-3 mt-2 grid ">
                {Object.values(resource.roles).map(role => (
                  <li
                    key={role.key}
                    className="flex justify-between items-center p-3 bg-gray-100 rounded-md shadow-sm">
                    <span className="font-bold text-gray-700">{role.name}</span>
                    <section className="text-gray-600 flex gap-1">
                      <span className="text-xs md:text-sm ml-1">
                        Allowed Permissions:
                      </span>
                      {role.permissions.map(pr => (
                        <span
                          key={pr}
                          className="bg-orange-800 text-white text-xs uppercase rounded-md shadow font-bold flex items-center justify-center px-2">
                          {pr}
                        </span>
                      ))}
                    </section>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

ResourceTree.propTypes = {
  resourcesData: PropTypes.array.isRequired,
};

export default ResourceTree;

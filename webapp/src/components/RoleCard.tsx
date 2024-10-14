import PropTypes from 'prop-types';
import React from 'react';

interface Role {
  key: string;
  name: string;
  permissions: string[];
  description?: string;
  id?: string;
}

interface RoleCardProps {
  rolesData: Role[];
}

const RoleCard: React.FC<RoleCardProps> = ({ rolesData }) => {
  if (rolesData.length === 0)
    return <p className="text-red-500 text-center">No roles available.</p>;

  const groupPermissions = (permissions: string[]) => {
    const grouped: { [key: string]: string[] } = {
      issue: [],
      repository: [],
      pull_request: [],
    };

    permissions.forEach(permission => {
      const [action, resource] = permission.split(':');
      if (grouped[resource]) {
        grouped[resource].push(action);
      }
    });

    return grouped;
  };

  return (
    <div className="p-6 bg-gray-100 rounded-lg shadow-lg mt-5 w-full h-ull">
      <h2 className="mb-6 text-3xl font-bold text-left text-gray-800">
        User & Roles Overview
      </h2>

      <ul className="grid grid-cols-1 md:grid-cols-3 gap-5 ">
        {rolesData.map(role => {
          const groupedPermissions = groupPermissions(role.permissions);

          return (
            <li
              key={role.id}
              className="bg-white rounded-lg p-5 shadow-md transition-transform transform hover:scale-105">
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-semibold text-lg text-gray-800 capitalize">
                    {role.name}
                  </span>
                </div>
                <span className="text-sm font-bold text-gray-700">
                  {role.permissions.length} Permissions
                </span>
              </div>

              <div className="mt-3">
                {Object.entries(groupedPermissions).map(
                  ([resource, actions]) =>
                    actions.length > 0 && (
                      <div key={resource} className="mt-2">
                        <h4 className="font-medium text-gray-700">
                          {resource.charAt(0).toUpperCase() + resource.slice(1)}
                          :
                        </h4>
                        <p className="text-gray-600 text-sm">
                          {actions.join(', ')}: {role.name} can{' '}
                          {actions.join(', ')} {resource}(s).
                        </p>
                      </div>
                    )
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

RoleCard.propTypes = {
  rolesData: PropTypes.array.isRequired,
};

export default RoleCard;

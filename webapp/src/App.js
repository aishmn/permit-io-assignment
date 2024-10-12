import './App.css';

import * as d3 from 'd3';

import React, { useEffect, useState } from 'react';

import axios from 'axios';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPolicyData();
  }, []);

  const fetchPolicyData = async () => {
    try {
      const response = await axios.get(
        'http://localhost:8000/api/v1/resources/rebac-data'
      );
      drawChart(response.data);
    } catch (error) {
      setError('Failed to fetch policy data. Please try again later.');
      console.error('Error fetching policy data:', error);
    } finally {
      setLoading(false);
    }
  };

  const drawChart = policyData => {
    const width = 1000;
    const height = 800;

    d3.select('#d3-container').select('svg').remove();

    const svg = d3
      .select('#d3-container')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .style('background', '#f9fafb')
      .style('border', '1px solid #ccc')
      .style('display', 'flex')
      .style('justify-content', 'center')
      .style('align-items', 'center')
      .style('border-radius', '8px');

    const nodes = [];
    const links = [];

    policyData.forEach(item => {
      nodes.push({ id: item.role, type: 'role' });
      nodes.push({ id: item.resourceType, type: 'resource' });

      item.actions.forEach(action => {
        links.push({ source: item.role, target: item.resourceType, action });
      });
    });

    const uniqueNodes = Array.from(
      new Set(nodes.map(node => JSON.stringify(node)))
    ).map(node => JSON.parse(node));

    const nodeMap = {};
    uniqueNodes.forEach(node => {
      nodeMap[node.id] = node;
    });

    const link = svg
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links)
      .enter()
      .append('line')
      .attr('stroke-width', 2)
      .attr('stroke', '#aaa')
      .attr('marker-end', 'url(#arrow)');

    const node = svg
      .append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(uniqueNodes)
      .enter()
      .append('circle')
      .attr('r', 20)
      .attr('fill', d => (d.type === 'role' ? '#0366d6' : '#10B981'))
      .style('stroke', '#fff')
      .style('stroke-width', 2)
      .call(
        d3
          .drag()
          .on('start', dragStarted)
          .on('drag', dragged)
          .on('end', dragEnded)
      );

    svg
      .append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(uniqueNodes)
      .enter()
      .append('text')
      .attr('dy', 4)
      .attr('text-anchor', 'middle')
      .attr('fill', '#374151')
      .style('font-family', 'Arial')
      .style('font-size', '12px')
      .text(d => d.id);

    svg
      .append('defs')
      .append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 0 10 10')
      .attr('refX', 15)
      .attr('refY', 5)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,0 L0,10 L10,5 Z')
      .attr('fill', '#aaa');

    const simulation = d3
      .forceSimulation(uniqueNodes)
      .force(
        'link',
        d3
          .forceLink()
          .id(d => d.id)
          .distance(120)
          .strength(1)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('tick', () => {
        link
          .attr('x1', d => nodeMap[d.source].x)
          .attr('y1', d => nodeMap[d.source].y)
          .attr('x2', d => nodeMap[d.target].x)
          .attr('y2', d => nodeMap[d.target].y);

        node.attr('cx', d => d.x).attr('cy', d => d.y);

        svg
          .selectAll('.labels text')
          .attr('x', d => d.x)
          .attr('y', d => d.y);
      });

    function dragStarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnded(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  };

  return (
    <div className="App ">
      <div className="container mx-auto p-5 flex-row">
        <Navbar />

        {loading ? (
          <p className="text-center text-gray-500">Loading...</p>
        ) : error ? (
          <p className="text-center text-red-500">{error}</p>
        ) : (
          <div
            id="d3-container"
            className="bg-white shadow-lg p-5 rounded-md mx-auto w-full h-full md:pl-[15%]"></div>
        )}
      </div>
    </div>
  );
}

const Navbar = () => {
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-white text-lg font-semibold">
          ReBAC Visualization Assignment
        </div>
        <div>
          <a
            href="/login"
            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
            Login
          </a>
          <a
            href="/signup"
            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium ml-4">
            Signup
          </a>
        </div>
      </div>
    </nav>
  );
};

export default App;

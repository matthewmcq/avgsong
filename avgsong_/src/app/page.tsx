import React from 'react';
import Layout from './layout';
import HomePage from '../pages/home';
import Top200 from '../pages/top200';
import YourAvg from '../pages/youravg';

const AppPage: React.FC = () => {
  return (
    <Layout>
      <HomePage />
      <Top200 />
      <YourAvg />
    </Layout>
  );
};

export default AppPage;
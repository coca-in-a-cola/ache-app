import React from 'react';

import { News } from '../../components/Pages/News';
// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: News,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <News {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  entity: "/api/news"
};

export const Maps = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Maps.args = {
  entity: "/api/maps/map_rzhm"
};
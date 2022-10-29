import React from 'react';

import { Main } from '../../components/Pages/Main';
// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Main,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <Main {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  location: ""
};

export const Services = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Services.args = {
  location: "services"
};
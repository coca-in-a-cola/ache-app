import React from 'react';

import { FlatMenu } from '../components/FlatMenu';
// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: FlatMenu,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <FlatMenu {...args} />;

export const Main = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Main.args = {
    path: "",
};

export const Services = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Services.args = {
  path: "/services",
};

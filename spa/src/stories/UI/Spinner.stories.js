import React from 'react';

import { Spinner } from '../../components/UI/Spinner';

// More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: Spinner,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <Spinner {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
  children: "Загрузка..."
};
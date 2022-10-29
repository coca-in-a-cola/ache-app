import React from 'react';

import { ReadCard } from '../../components/Modals/ReadCard'
    // More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: ReadCard,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <ReadCard {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
    onSubmit: (number) => alert("Введён пропуск " + number),
  onCancel: () => alert("Пользователь отменил ввод")
};
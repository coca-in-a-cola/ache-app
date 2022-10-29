import React from 'react';

import { FormTask } from '../../components/Modals/FormTask'
    // More on default export: https://storybook.js.org/docs/react/writing-stories/introduction#default-export
export default {
  component: FormTask,
  // More on argTypes: https://storybook.js.org/docs/react/api/argtypes
};

// More on component templates: https://storybook.js.org/docs/react/writing-stories/introduction#using-args
const Template = (args) => <FormTask {...args} />;

export const Default = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
Default.args = {
    onSubmit: (data) => alert("Получили данные " + JSON.stringify(data)),
    onCancel: () => alert("Пользователь отменил ввод")
};

export const WithFields = Template.bind({});
// More on args: https://storybook.js.org/docs/react/writing-stories/args
WithFields.args = {
    fields: [
      {
        name: "Date",
        label: "Год",
        type: "numeric",
        required: true
      },
      {
        name: "For",
        label: "Место требования",
        type: "text",
        placeholder: "Военкомат",
        required: true
      },
      {
        name: "Comment",
        label: "Дополнительная информация (комментарий)",
        type: "text",
        required: false
      },
    ],
    onSubmit: (data) => alert("Получили данные " + JSON.stringify(data)),
    onCancel: () => alert("Пользователь отменил ввод")
};
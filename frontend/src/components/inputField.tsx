import React from 'react';
import { View, TextInput, Text } from 'react-native';

type InputFieldProps = {
  icon: React.ReactNode;
  placeholder: string;
  secureTextEntry?: boolean;
};

const InputField: React.FC<InputFieldProps> = ({ icon, placeholder, secureTextEntry }) => {
  return (
    <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
      {icon} 
      <TextInput
        placeholder={placeholder}
        secureTextEntry={secureTextEntry}
        className="flex-1 ml-3"
      />
    </View>
  );
};

export default InputField;

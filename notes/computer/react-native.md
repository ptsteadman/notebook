# React Native

## Clearing up build issues:

```
rm -rf node_modules
npm i
```

## Clearing up Android build issues:

For android:

Things that need to be the same
    - Android build tools / sdk version
    - npm package numbers
    - 
 


```
cd android
./gradlew clean
cd ..
react-native run-android
```

## Clearing up iOS build issues

Product -> Clean

## Stripe RN without ejecting from expo

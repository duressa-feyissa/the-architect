import 'package:architect/features/architect/presentations/bloc/post/post_bloc.dart';
import 'package:architect/features/architect/presentations/bloc/user/user_bloc.dart';
import 'package:architect/injection_container.dart';
import 'package:architect/simple_bloc_observer.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'features/architect/presentations/bloc/auth/auth_bloc.dart';
import 'features/architect/presentations/bloc/type/type_bloc.dart';
import 'features/architect/presentations/page/login.dart';
import 'injection_container.dart' as di;

void main() async {
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Color.fromARGB(255, 236, 238, 244),
    statusBarIconBrightness: Brightness.dark,
  ));

  Bloc.observer = const SimpleBlocObserver();

  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  await di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (context) => sl<PostBloc>()
            ..add(
              const AllPosts(tags: [], search: ''),
            ),
        ),
        BlocProvider<AuthBloc>(
          create: (context) => sl<AuthBloc>(),
        ),
        BlocProvider<UserBloc>(
          create: (context) => sl<UserBloc>(),
        ),
        BlocProvider<TypeBloc>(
          create: (context) => sl<TypeBloc>()..add(GetType()),
        )
      ],
      child: MaterialApp(
        title: 'Architect',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const Login(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}

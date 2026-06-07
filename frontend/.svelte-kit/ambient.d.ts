
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/private';
 * 
 * console.log(ENVIRONMENT); // => "production"
 * console.log(PUBLIC_BASE_URL); // => throws error during build
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/private' {
	export const SVELTEKIT_FORK: string;
	export const NODE_ENV: string;
	export const HISTFILE: string;
	export const npm_config_global_prefix: string;
	export const NVM_CD_FLAGS: string;
	export const npm_execpath: string;
	export const PWD: string;
	export const npm_config_globalconfig: string;
	export const GDMSESSION: string;
	export const npm_config_init_module: string;
	export const QT_ACCESSIBILITY: string;
	export const npm_lifecycle_event: string;
	export const npm_package_version: string;
	export const VTE_VERSION: string;
	export const SSH_AUTH_SOCK: string;
	export const QT_IM_MODULE: string;
	export const SSH_AGENT_LAUNCHER: string;
	export const npm_lifecycle_script: string;
	export const NVM_DIR: string;
	export const COLORTERM: string;
	export const npm_config_user_agent: string;
	export const npm_package_json: string;
	export const DBUS_SESSION_BUS_ADDRESS: string;
	export const OLDPWD: string;
	export const SYSTEMD_EXEC_PID: string;
	export const npm_config_userconfig: string;
	export const __MISE_DIFF: string;
	export const SESSION_MANAGER: string;
	export const GTK_MODULES: string;
	export const GNOME_SHELL_SESSION_MODE: string;
	export const NVM_INC: string;
	export const LESSCLOSE: string;
	export const MISE_SHELL: string;
	export const PATH: string;
	export const COLOR: string;
	export const DESKTOP_SESSION: string;
	export const HISTFILESIZE: string;
	export const LANGUAGE: string;
	export const npm_command: string;
	export const LOGNAME: string;
	export const HOME: string;
	export const __MISE_SESSION: string;
	export const INIT_CWD: string;
	export const __MISE_ORIG_PATH: string;
	export const KAMAL_REGISTRY_PASSWORD: string;
	export const XDG_SESSION_TYPE: string;
	export const npm_node_execpath: string;
	export const SHLVL: string;
	export const USER: string;
	export const XDG_DATA_DIRS: string;
	export const LESSOPEN: string;
	export const GNOME_DESKTOP_SESSION_ID: string;
	export const SHELL: string;
	export const npm_config_node_gyp: string;
	export const npm_config_noproxy: string;
	export const npm_config_npm_version: string;
	export const EDITOR: string;
	export const IM_CONFIG_PHASE: string;
	export const WAYLAND_DISPLAY: string;
	export const npm_config_prefix: string;
	export const USERNAME: string;
	export const XDG_CONFIG_DIRS: string;
	export const TERM: string;
	export const npm_config_cache: string;
	export const NODE: string;
	export const XDG_MENU_PREFIX: string;
	export const npm_package_name: string;
	export const GNOME_TERMINAL_SCREEN: string;
	export const XDG_SESSION_CLASS: string;
	export const GNOME_TERMINAL_SERVICE: string;
	export const GNOME_SETUP_DISPLAY: string;
	export const _: string;
	export const XDG_CURRENT_DESKTOP: string;
	export const XDG_RUNTIME_DIR: string;
	export const DISPLAY: string;
	export const HISTSIZE: string;
	export const PI_CODING_AGENT: string;
	export const LANG: string;
	export const NVM_BIN: string;
	export const XMODIFIERS: string;
	export const XDG_SESSION_DESKTOP: string;
	export const npm_config_local_prefix: string;
	export const XAUTHORITY: string;
	export const LS_COLORS: string;
}

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/public';
 * 
 * console.log(ENVIRONMENT); // => throws error during build
 * console.log(PUBLIC_BASE_URL); // => "http://site.com"
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * 
 * console.log(env.ENVIRONMENT); // => "production"
 * console.log(env.PUBLIC_BASE_URL); // => undefined
 * ```
 */
declare module '$env/dynamic/private' {
	export const env: {
		SVELTEKIT_FORK: string;
		NODE_ENV: string;
		HISTFILE: string;
		npm_config_global_prefix: string;
		NVM_CD_FLAGS: string;
		npm_execpath: string;
		PWD: string;
		npm_config_globalconfig: string;
		GDMSESSION: string;
		npm_config_init_module: string;
		QT_ACCESSIBILITY: string;
		npm_lifecycle_event: string;
		npm_package_version: string;
		VTE_VERSION: string;
		SSH_AUTH_SOCK: string;
		QT_IM_MODULE: string;
		SSH_AGENT_LAUNCHER: string;
		npm_lifecycle_script: string;
		NVM_DIR: string;
		COLORTERM: string;
		npm_config_user_agent: string;
		npm_package_json: string;
		DBUS_SESSION_BUS_ADDRESS: string;
		OLDPWD: string;
		SYSTEMD_EXEC_PID: string;
		npm_config_userconfig: string;
		__MISE_DIFF: string;
		SESSION_MANAGER: string;
		GTK_MODULES: string;
		GNOME_SHELL_SESSION_MODE: string;
		NVM_INC: string;
		LESSCLOSE: string;
		MISE_SHELL: string;
		PATH: string;
		COLOR: string;
		DESKTOP_SESSION: string;
		HISTFILESIZE: string;
		LANGUAGE: string;
		npm_command: string;
		LOGNAME: string;
		HOME: string;
		__MISE_SESSION: string;
		INIT_CWD: string;
		__MISE_ORIG_PATH: string;
		KAMAL_REGISTRY_PASSWORD: string;
		XDG_SESSION_TYPE: string;
		npm_node_execpath: string;
		SHLVL: string;
		USER: string;
		XDG_DATA_DIRS: string;
		LESSOPEN: string;
		GNOME_DESKTOP_SESSION_ID: string;
		SHELL: string;
		npm_config_node_gyp: string;
		npm_config_noproxy: string;
		npm_config_npm_version: string;
		EDITOR: string;
		IM_CONFIG_PHASE: string;
		WAYLAND_DISPLAY: string;
		npm_config_prefix: string;
		USERNAME: string;
		XDG_CONFIG_DIRS: string;
		TERM: string;
		npm_config_cache: string;
		NODE: string;
		XDG_MENU_PREFIX: string;
		npm_package_name: string;
		GNOME_TERMINAL_SCREEN: string;
		XDG_SESSION_CLASS: string;
		GNOME_TERMINAL_SERVICE: string;
		GNOME_SETUP_DISPLAY: string;
		_: string;
		XDG_CURRENT_DESKTOP: string;
		XDG_RUNTIME_DIR: string;
		DISPLAY: string;
		HISTSIZE: string;
		PI_CODING_AGENT: string;
		LANG: string;
		NVM_BIN: string;
		XMODIFIERS: string;
		XDG_SESSION_DESKTOP: string;
		npm_config_local_prefix: string;
		XAUTHORITY: string;
		LS_COLORS: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://example.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.ENVIRONMENT); // => undefined, not public
 * console.log(env.PUBLIC_BASE_URL); // => "http://example.com"
 * ```
 * 
 * ```
 * 
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
